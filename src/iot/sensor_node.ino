/*
 * Pytho IoT - Sensore per Orti Intelligenti
 * ESP8266 / ESP32
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// Configurazione WiFi
const char* ssid = "MYZUBSTER_WIFI";
const char* password = "pytho2026";

// Configurazione MQTT
const char* mqtt_server = "mqtt.myzubster.com";
const int mqtt_port = 1883;

// Sensori
#define DHTPIN 4
#define DHTTYPE DHT22
#define SOIL_PIN A0
#define LIGHT_PIN A1

DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

// Variabili sensori
float temperature = 0;
float humidity = 0;
float soil_moisture = 0;
float light_level = 0;

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  dht.begin();
  pinMode(SOIL_PIN, INPUT);
  pinMode(LIGHT_PIN, INPUT);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("Pytho_Sensor_01")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void read_sensors() {
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  soil_moisture = (1023 - analogRead(SOIL_PIN)) / 1023.0 * 100;
  light_level = analogRead(LIGHT_PIN) / 1023.0 * 1000;
  
  Serial.println("📊 Sensori:");
  Serial.print("  🌡️ Temperatura: "); Serial.print(temperature); Serial.println("°C");
  Serial.print("  💧 Umidità: "); Serial.print(humidity); Serial.println("%");
  Serial.print("  🌱 Umidità terreno: "); Serial.print(soil_moisture); Serial.println("%");
  Serial.print("  ☀️ Luce: "); Serial.print(light_level); Serial.println(" lux");
}

void publish_data() {
  char msg[100];
  
  snprintf(msg, 100, "%.1f", temperature);
  client.publish("pytho/sensors/temperature", msg);
  
  snprintf(msg, 100, "%.1f", humidity);
  client.publish("pytho/sensors/humidity", msg);
  
  snprintf(msg, 100, "%.1f", soil_moisture);
  client.publish("pytho/sensors/soil_moisture", msg);
  
  snprintf(msg, 100, "%.1f", light_level);
  client.publish("pytho/sensors/light", msg);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  read_sensors();
  publish_data();
  
  delay(60000);
}
