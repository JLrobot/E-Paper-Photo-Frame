# E-Paper Photo Frame

A handmade digital photo frame built with an ESP32 and a 4.2" e-paper display. Every time power is connected, the frame automatically advances to the next photo. The image stays visible even without power — no energy needed to hold the picture.

<img width="2394" height="2759" alt="E-Paper-Picture" src="https://github.com/user-attachments/assets/232c4cc5-5f72-48b9-97cf-dfb666b2b0bd" />


## Features

- 📷 Cycles through up to 66 photos stored on the ESP32
- 🔋 Image persists without power (e-paper technology)
- 🔌 New photo on every power cycle — no buttons, no apps
- 🖨️ 3D-printed frame with custom design
- 🐍 Python script to convert JPG/PNG photos to the required binary format

---

## Hardware

| Component | Description | Link |
|---|---|---|
| ESP32 Dev Module | Hailege ESP32-ESP32D, 38-Pin, USB-C, WiFi + Bluetooth | [Amazon](https://www.amazon.de/dp/B0DRFSSB88) |
| E-Paper Display | WaveShare 4.2" Pico-ePaper-4.2, 400×300px, Black/White, SPI | [Eckstein](https://eckstein-shop.de/WaveShare-42inch-E-Paper-E-Ink-Display-Module-for-Raspberry-Pi-Pico-400x300-Black-White-4-Grayscale-SPI) |
| Micro USB Cable | Amazon Basics, for power supply | [Amazon](https://www.amazon.de/Amazon-Basics-%C3%9Cbertragungsgeschwindigkeit-vergoldeten-Steckern/dp/B071S5NTDR) |
| Power Bank | Any USB power bank (make sure it doesn't auto-shutoff at low current) | — |


---

## Wiring

| E-Paper Display | ESP32 GPIO |
|---|---|
| VCC | 3.3V |
| GND | GND |
| DIN (MOSI) | GPIO 23 |
| CLK | GPIO 18 |
| CS | GPIO 5 |
| DC | GPIO 17 |
| RST | GPIO 16 |
| BUSY | GPIO 4 |

---

## How It Works

1. Photos are converted to 15,000-byte binary files using the Python script
2. Binary files are uploaded to the ESP32 flash via LittleFS
3. On every power-on, the ESP32 loads the next image and displays it
4. The current image index is saved to flash so it persists across power cycles
5. The display holds the image without any power draw

---

## Setup

### 1. Arduino IDE

Install the following libraries via Library Manager:
- `GxEPD2` by Jean-Marc Zingg
- `Adafruit GFX`

Board settings:
- Board: `ESP32 Dev Module`
- Partition Scheme: `Huge APP (3MB No OTA/1MB SPIFFS)`

Upload `epaper_flash_direct.ino` to your ESP32.

### 2. Convert Photos

Install Python dependencies:
```bash
pip install Pillow numpy
```

Place your portrait-orientation JPG/PNG photos in the input folder, then run:
```bash
python epaper_converter_fixed_rotation.py
```

The script will:
- Convert and optimize each image (contrast, sharpness, dithering)
- Save binary files numbered `bild1.bin`, `bild2.bin`, etc.
- Archive the originals automatically

### 3. Upload Photos to ESP32

- Copy all `.bin` files into the `data/` folder of the Arduino sketch
- In Arduino IDE: `Ctrl + Shift + P` → **"Upload LittleFS"**
- Done!

---

## Image Converter Settings

You can tune the image quality in `epaper_converter_fixed_rotation.py`:

```python
CONTRAST   = 1.6   # Contrast (1.0 = default)
BRIGHTNESS = 1.1   # Brightness (1.0 = default)
SHARPNESS   = 2.0   # Sharpness (1.0 = default)
```

---

## File Structure

```
epaper-photo-frame/
├── README.md
├── arduino/
│   └── epaper_flash_direct.ino
├── python/
    └── epaper_converter_fixed_rotation.py

```

---

## Built With

- [GxEPD2](https://github.com/ZinggJM/GxEPD2) — E-Paper display library
- [LittleFS](https://github.com/lorol/LITTLEFS) — File system for ESP32
- [Pillow](https://python-pillow.org/) — Image processing in Python
- Bambu Lab A1 — 3D-printed enclosure

---

## License

MIT License — feel free to use, modify and share.
