#include <GxEPD2_BW.h>
#include <LittleFS.h>

#define SPI_MOSI 23
#define SPI_CLK 18
#define SPI_CS 5
#define SPI_DC 17
#define SPI_RST 16
#define SPI_BUSY 4
#define MAX_IMAGES 66

GxEPD2_BW<GxEPD2_420_GDEY042T81, GxEPD2_420_GDEY042T81::HEIGHT> display(
  GxEPD2_420_GDEY042T81(SPI_CS, SPI_DC, SPI_RST, SPI_BUSY)
);

String imageFiles[MAX_IMAGES];
int imageCount = 0;
uint8_t imgBuffer[15000];

int loadCurrentIndex() {
  File f = LittleFS.open("/index.txt", "r");
  if (!f) return 0;
  int val = f.parseInt();
  f.close();
  return val;
}

void saveCurrentIndex(int idx) {
  File f = LittleFS.open("/index.txt", "w");
  if (!f) return;
  f.print(idx);
  f.close();
}

void listImages() {
  File root = LittleFS.open("/");
  File file = root.openNextFile();
  while (file && imageCount < MAX_IMAGES) {
    String name = String(file.name());
    if (!name.startsWith("/")) name = "/" + name;
    if (file.size() == 15000) {
      imageFiles[imageCount++] = name;
    }
    file = root.openNextFile();
  }
  Serial.printf("%d Bilder gefunden\n", imageCount);
}

bool loadBIN(const char* path) {
  File f = LittleFS.open(path, "r");
  if (!f) return false;
  if (f.size() != 15000) { f.close(); return false; }
  f.read(imgBuffer, 15000);
  f.close();
  return true;
}

void showImage(const char* path) {
  if (!loadBIN(path)) return;
  display.setFullWindow();
  display.firstPage();
  do {
    display.fillScreen(GxEPD_WHITE);
    display.drawBitmap(0, 0, imgBuffer, 400, 300, GxEPD_BLACK);
  } while (display.nextPage());
}

void setup() {
  Serial.begin(115200);
  delay(100);

  SPI.begin(SPI_CLK, -1, SPI_MOSI, SPI_CS);

  if (!LittleFS.begin(true)) {
    Serial.println("LittleFS Fehler!");
    return;
  }

  display.init(9600, true, 2, false);

  listImages();

  if (imageCount == 0) {
    Serial.println("Keine Bilder gefunden!");
    return;
  }

  int currentImage = loadCurrentIndex();
  if (currentImage >= imageCount) currentImage = 0;

  Serial.printf("Zeige Bild %d von %d\n", currentImage + 1, imageCount);
  showImage(imageFiles[currentImage].c_str());

  display.hibernate();

  currentImage = (currentImage + 1) % imageCount;
  saveCurrentIndex(currentImage);
  Serial.printf("Nächstes Bild: %d\n", currentImage + 1);
}

void loop() {}