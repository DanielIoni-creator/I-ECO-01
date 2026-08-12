# 🌱 Pytho IoT - Sensori per Orti Intelligenti

## 📋 Architettura

ESP32/ESP8266 → MQTT → Gateway → Dashboard

## 🔧 Hardware

- ESP32 o ESP8266
- Sensore DHT22 (temperatura/umidità)
- Sensore umidità terreno capacitivo
- Sensore luce (fotoresistore)

## 📡 Topic MQTT

- pytho/sensors/temperature
- pytho/sensors/humidity
- pytho/sensors/soil_moisture
- pytho/sensors/light
