/**
 * 🤖 MyZubster AI Companion v1.0
 * ESP32 + Pytho AI = Personal AI Assistant
 * 
 * Connessione a MyZubster Gateway per chat vocale
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ============================================
// CONFIGURAZIONE
// ============================================

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASSWORD";

const char* GATEWAY_URL = "http://YOUR_IP:3001";
const char* CHAT_ENDPOINT = "/api/pytho/chat";

#define LED_BUILTIN 2
#define BUTTON_PIN 0

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ============================================
// SETUP
// ============================================

void setup() {
    Serial.begin(115200);
    Serial.println("🤖 MyZubster AI Companion v1.0");
    
    // LED e pulsante
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    
    // Display
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("❌ Display non trovato!");
        while (true);
    }
    
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("👽 MyZubster");
    display.println("AI Companion");
    display.println("v1.0");
    display.println("");
    display.println("Avvio...");
    display.display();
    
    // WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("✅ WiFi connesso!");
    display.println("✅ WiFi OK");
    display.display();
    
    // Pronto
    digitalWrite(LED_BUILTIN, LOW);
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("👽 Pytho");
    display.println("Pronto!");
    display.println("");
    display.println("🔊 Parla o premi");
    display.println("il pulsante");
    display.display();
    
    Serial.println("✅ Pronto!");
}

// ============================================
// LOOP
// ============================================

void loop() {
    if (digitalRead(BUTTON_PIN) == LOW) {
        delay(100);
        if (digitalRead(BUTTON_PIN) == LOW) {
            handleInteraction();
        }
    }
    
    if (Serial.available()) {
        String input = Serial.readString();
        input.trim();
        if (input.length() > 0) {
            handleInput(input);
        }
    }
    delay(100);
}

// ============================================
// INTERAZIONE
// ============================================

void handleInteraction() {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("🎤 Ascolto...");
    display.println("");
    display.println("Parla ora");
    display.display();
    digitalWrite(LED_BUILTIN, HIGH);
    
    delay(2000); // Simula registrazione
    
    digitalWrite(LED_BUILTIN, LOW);
    handleInput("Ciao Pytho! Come stai?");
}

void handleInput(String query) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("🧠 Penso...");
    display.println("");
    display.println("⏳ Elaborazione");
    display.display();
    
    String response = callPythoAI(query);
    
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("🔊 Pytho:");
    display.println("");
    
    int len = response.length();
    int pos = 0;
    int line = 0;
    while (pos < len && line < 4) {
        String lineText = response.substring(pos, min(pos + 20, len));
        display.println(lineText);
        pos += 20;
        line++;
    }
    display.display();
    
    Serial.println("🔊: " + response);
    delay(3000);
    
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("👽 Pronto!");
    display.println("");
    display.println("🔊 Parla o premi");
    display.println("il pulsante");
    display.display();
}

// ============================================
// PYTHO AI
// ============================================

String callPythoAI(String message) {
    HTTPClient http;
    String url = String(GATEWAY_URL) + String(CHAT_ENDPOINT);
    
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    
    String payload = "{\"message\":\"" + message + "\"}";
    int httpResponseCode = http.POST(payload);
    
    String response = "👽 Non ho capito. Riprova!";
    if (httpResponseCode > 0) {
        String json = http.getString();
        DynamicJsonDocument doc(1024);
        deserializeJson(doc, json);
        response = doc["response"].as<String>();
        if (response.length() == 0) {
            response = doc["pytho_says"].as<String>();
        }
    } else {
        Serial.println("❌ Errore: " + String(httpResponseCode));
    }
    
    http.end();
    return response;
}
