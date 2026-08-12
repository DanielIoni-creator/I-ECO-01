/**
 * 🔧 MyZubster AI Companion - Configurazione
 * Modifica questi valori prima di caricare il firmware
 */

#ifndef CONFIG_H
#define CONFIG_H

// WiFi Credentials
#define WIFI_SSID "YOUR_WIFI"
#define WIFI_PASSWORD "YOUR_PASSWORD"

// MyZubster Gateway
#define GATEWAY_URL "http://YOUR_IP:3001"
#define CHAT_ENDPOINT "/api/pytho/chat"

// Pin Definitions
#define LED_BUILTIN 2
#define BUTTON_PIN 0
#define MIC_PIN 34
#define SPEAKER_PIN 25

// OLED Display
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Audio Settings
#define VOLUME 50
#define SAMPLE_RATE 16000

#endif
