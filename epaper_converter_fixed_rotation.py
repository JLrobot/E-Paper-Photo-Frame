from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import os
import glob
import shutil

# ============================================================
# CONFIGURATION — adjust these paths to your setup
# ============================================================
INPUT_FOLDER   = r"C:\Users\YourName\Desktop\epaper\1_input"
OUTPUT_FOLDER  = r"C:\Users\YourName\Desktop\epaper\2_output"
ARCHIVE_FOLDER = r"C:\Users\YourName\Desktop\epaper\3_archive"

# Image quality settings
CONTRAST    = 1.6   # 1.0 = default, higher = more contrast
BRIGHTNESS  = 1.1   # 1.0 = default, higher = brighter
SHARPNESS   = 2.0   # 1.0 = default, higher = sharper
# ============================================================

DISPLAY_W = 300
DISPLAY_H = 400

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# Find all JPG and PNG files (no duplicates)
alle = []
gesehen = set()
for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
    for f in glob.glob(os.path.join(INPUT_FOLDER, ext)):
        lower = f.lower()
        if lower not in gesehen:
            gesehen.add(lower)
            alle.append(f)

dateien = sorted(alle)

if not dateien:
    print(f"No images found in: {INPUT_FOLDER}")
    exit()

print(f"{len(dateien)} images found\n")

# Find highest existing number in output folder
existierende = glob.glob(os.path.join(OUTPUT_FOLDER, "bild*.bin"))
if existierende:
    nummern = []
    for e in existierende:
        name = os.path.basename(e)
        try:
            num = int(name.replace("bild", "").replace(".bin", ""))
            nummern.append(num)
        except:
            pass
    start_index = max(nummern) + 1
else:
    start_index = 1

print(f"Starting numbering at bild{start_index}.bin\n")

erfolgreich = []

for i, pfad in enumerate(dateien):
    dateiname = os.path.basename(pfad)
    bildnummer = start_index + i
    print(f"Converting ({i+1}/{len(dateien)}): {dateiname} → bild{bildnummer}.bin")

    try:
        # STEP 1: Copy original to archive
        archiv_ziel = os.path.join(ARCHIVE_FOLDER, dateiname)
        if os.path.exists(archiv_ziel):
            name, ext = os.path.splitext(dateiname)
            archiv_ziel = os.path.join(ARCHIVE_FOLDER, f"{name}_2{ext}")
        shutil.copy2(pfad, archiv_ziel)
        print(f"  → Archive: {os.path.basename(archiv_ziel)}")

        # STEP 2: Load and process image
        img = Image.open(pfad)
        img = ImageOps.exif_transpose(img)
        img = img.convert('L')

        # Enhance image quality
        img = ImageEnhance.Brightness(img).enhance(BRIGHTNESS)
        img = ImageEnhance.Contrast(img).enhance(CONTRAST)
        img = ImageEnhance.Sharpness(img).enhance(SHARPNESS)

        # Auto-levels for maximum contrast
        img = ImageOps.autocontrast(img, cutoff=2)

        # Scale to 300x400 keeping aspect ratio
        img.thumbnail((DISPLAY_W, DISPLAY_H), Image.LANCZOS)

        # Black background, center image
        background = Image.new('L', (DISPLAY_W, DISPLAY_H), 0)
        x = (DISPLAY_W - img.width) // 2
        y = (DISPLAY_H - img.height) // 2
        background.paste(img, (x, y))

        # Convert to black & white with dithering
        bw = background.convert('1', dither=Image.FLOYDSTEINBERG)

        # Rotate for correct display orientation
        bw = bw.rotate(-90, expand=True)

        # Pack bits → 15000 bytes (400x300 / 8)
        pixels = np.array(bw)
        pixels = 1 - pixels
        packed = np.packbits(pixels.flatten())

        if len(packed) != 15000:
            print(f"  ERROR: Wrong size {len(packed)} bytes (expected 15000)")
            continue

        # STEP 3: Save .bin file
        output_path = os.path.join(OUTPUT_FOLDER, f"bild{bildnummer}.bin")
        packed.tofile(output_path)
        print(f"  → bild{bildnummer}.bin saved")

        erfolgreich.append(pfad)

    except Exception as e:
        print(f"  ERROR: {e}")

# STEP 4: Delete originals from input folder
print(f"\nDeleting originals from input folder...")
for pfad in erfolgreich:
    os.remove(pfad)
    print(f"  {os.path.basename(pfad)} deleted")

print(f"\nDone! {len(erfolgreich)} images converted.")
print(f".bin files in: {OUTPUT_FOLDER}")
print(f"Originals in:  {ARCHIVE_FOLDER}")
