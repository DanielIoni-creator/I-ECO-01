# 🏥 MyZubster Nurse Robots

Robot Open Source per assistenza sanitaria e monitoraggio pazienti.

## 🤖 Progetti

### 1. Vital Signs Monitor (3 XMR)
Monitoraggio parametri vitali (frequenza cardiaca, ossigenazione, temperatura) con sensori IoT.

### 2. Medication Dispenser (2 XMR)
Distributore automatico di farmaci con controllo XMR.

### 3. Patient Call System (1 XMR)
Sistema di chiamata per pazienti con notifiche in tempo reale.

## Implementazioni bounty

- `monitor/vital_monitor.py`: letture Heart Rate, SpO2 e temperatura, allarmi configurabili,
  snapshot dashboard e log audit hash-chain per integrazione blockchain.
- `medication_dispenser.py`: dosaggio validato, autorizzazione QR, registro
  somministrazioni e riferimento wallet XMR.
- `patient_call_system.py`: pulsante wireless simulato, notifiche push,
  dashboard infermieri e storico chiamate.

## Test

```bash
cd robots/nurse
python -m unittest test_nurse_bounties.py
```

## 📦 Tecnologie
- Raspberry Pi / ESP32
- Sensori: Heart Rate, SpO2, Temperature
- Python / C++
- Monero RPC per pagamenti

## 💰 Bounty Attivi
Vedi le issue per i bounty disponibili.
