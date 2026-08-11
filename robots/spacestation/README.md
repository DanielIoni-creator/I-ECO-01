# 🛰️ MyZubster Space Station Robots

Robot Open Source per la gestione della Space Station, con focus su supporto vitale, monitoraggio ambientale e centrale energetica a fusione.

## 🤖 Progetti

### 1. Life Support System (6 XMR) — issue #106
Modulo di supporto vitale per la cabina:
- Controllo ossigeno (O2) e anidride carbonica (CO2)
- Monitoraggio purezza dell'acqua del circuito
- Controllo temperatura e umidita`
- Sistema di allarmi con soglie configurabili (warning/critical)
- Pubblicazione stato su dashboard via payload JSON

### 2. Fusion Power Integration - Pulsar Technology (15 XMR) — issue #134
Centrale a fusione aneutronica (Pulsar Sunbird) per l'alimentazione della stazione:
- Modello teorico di fusione per alimentazione stazione (D-T, D-D, D-He3, p-B11)
- Simulazione plasma con diagnostiche (T_i, T_e, n_e, tau_E, Q, pressione)
- Sistema di propulsione avanzata (Isp e spinta derivate dal plasma)
- Dashboard monitoraggio fusione (payload JSON)
- Hook di integrazione con AI Core (controllo chiuso)

## 📦 Tecnologie
- Python 3
- Sensori: O2, CO2, temperatura, umidita`, filtro acqua, plasma (T, n, tau_E)
- Dashboard: HTTP/MQTT/JSON (adapter iniettabile)
- Test: `unittest` (stdlib)

## 🧪 Test
```
cd I-ECO-01
python3 -m unittest robots.spacestation.life_support.test_life_support -v
python3 -m unittest robots.spacestation.fusion_power.test_fusion_power -v
```

## 💰 Bounty
Vedi le issue #106 e #134 per i dettagli dei bounty in XMR.
