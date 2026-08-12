# 🤖 Pytho Robot Giardiniere - Design Document

## 📋 Specifiche Tecniche

### Hardware
- **Controller**: Raspberry Pi 4 (4GB RAM)
- **Motori**: 2x motori DC con encoder
- **Sensori**: 
  - Ultrasonici (HC-SR04) per ostacoli
  - Sensore di umidità terreno
  - Sensore luce e temperatura
  - Telecamera (Raspberry Pi Camera v2)
- **Alimentazione**: Batteria LiPo 12V 10000mAh
- **Display**: OLED 1.3" per status

### Software
- **OS**: Raspberry Pi OS Lite
- **Framework**: ROS 2 (Robot Operating System)
- **AI**: TensorFlow Lite per riconoscimento piante
- **Comunicazione**: WebSocket per streaming

### Funzionalità
1. Navigazione autonoma nell'orto
2. Riconoscimento piante con AI
3. Monitoraggio crescita
4. Interazione vocale (Pytho AI)
5. Streaming video in tempo reale

## 📝 Roadmap

### Fase 1 (Settimana 1-2)
- [ ] Assemblaggio hardware
- [ ] Configurazione Raspberry Pi
- [ ] Installazione ROS 2

### Fase 2 (Settimana 3-4)
- [ ] Sviluppo navigazione
- [ ] Integrazione sensori
- [ ] Testing movimento

### Fase 3 (Settimana 5-6)
- [ ] Integrazione AI vision
- [ ] Riconoscimento piante
- [ ] Streaming video

### Fase 4 (Settimana 7-8)
- [ ] Integrazione con Pytho AI
- [ ] Testing completo
- [ ] Deployment

## 🔗 Risorse
- [ROS 2 Documentation](https://docs.ros.org)
- [TensorFlow Lite](https://www.tensorflow.org/lite)
- [Raspberry Pi Camera](https://www.raspberrypi.com/documentation/accessories/camera.html)
