/*
 * Pytho Luce e Suono - Esperienza Immersiva
 * Arduino / ESP32
 */

#include <FastLED.h>
#include <DFRobotDFPlayerMini.h>

// Configurazione LED
#define LED_PIN 6
#define NUM_LEDS 100
#define BRIGHTNESS 64

CRGB leds[NUM_LEDS];

// Configurazione MP3
SoftwareSerial mySoftwareSerial(10, 11);
DFRobotDFPlayerMini myDFPlayer;

// Modalità
enum Mode { RAINBOW, NATURE, PARTY, SLEEP };
Mode currentMode = RAINBOW;

void setup() {
  Serial.begin(115200);
  
  // Inizializza LED
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  
  // Inizializza MP3
  mySoftwareSerial.begin(9600);
  if (myDFPlayer.begin(mySoftwareSerial)) {
    myDFPlayer.volume(20);
    myDFPlayer.play(1);
  }
}

void loop() {
  switch(currentMode) {
    case RAINBOW:
      rainbow();
      break;
    case NATURE:
      nature();
      break;
    case PARTY:
      party();
      break;
    case SLEEP:
      sleep();
      break;
  }
  
  FastLED.show();
  delay(50);
}

void rainbow() {
  static uint8_t hue = 0;
  fill_rainbow(leds, NUM_LEDS, hue, 7);
  hue++;
}

void nature() {
  // Effetto natura (verde/azzurro)
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(120 + random(20), 200, random(100, 200));
  }
}

void party() {
  // Effetto party
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(random(255), 255, 255);
  }
}

void sleep() {
  // Effetto sleep (bassa intensità)
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(160, 100, 20);
  }
}
