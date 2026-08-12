# 🔗 Pytho Sistema Integrato

## Architettura

## Architettura

┌─────────────────────────────────────────────┐
│ Pytho System Integration │
├─────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ │
│ │ Robot │ │ IoT │ │ Display │ │
│ └─────────┘ └─────────┘ └─────────┘ │
│ │ │ │ │
│ ┌─────────────────────────────────────┐ │
│ │ MQTT / WebSocket │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
text


## Componenti

- **Orchestration**: Node.js + MQTT
- **Robot**: Python + ROS
- **IoT**: ESP32 + MQTT
- **Display**: React + Node.js
- **Luci/Suoni**: Arduino + FastLED
