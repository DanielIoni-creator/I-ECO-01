# 🛰️ MyZubster Space Station Robots

Robot Open Source per la gestione della Space Station, con focus su supporto vitale e monitoraggio ambientale.

## 🤖 Progetti

### 1. Life Support System (6 XMR) — issue #106
Modulo di supporto vitale per la cabina:
- Controllo ossigeno (O2) e anidride carbonica (CO2)
- Monitoraggio purezza dell'acqua del circuito
- Controllo temperatura e umidita`
- Sistema di allarmi con soglie configurabili (warning/critical)
- Pubblicazione stato su dashboard via payload JSON

## 📦 Tecnologie
- Python 3
- Sensori: O2, CO2, temperatura, umidita`, filtro acqua
- Dashboard: HTTP/MQTT/JSON (adapter iniettabile)
- Test: `unittest` (stdlib)

## 🧪 Test
```
cd I-ECO-01
python3 -m unittest robots.spacestation.life_support.test_life_support -v
```

## 💰 Bounty
Vedi la issue #106 per i dettagli del bounty in XMR.
