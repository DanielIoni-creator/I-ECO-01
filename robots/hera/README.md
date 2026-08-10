# 🧹 Hera - Robot per Pulizia e Manutenzione

Robot Open Source per la pulizia e la gestione automatica degli spazi.

## 🤖 Progetti

### 1. Hera Cleaner (3 XMR)
Robot aspirapolvere e lavapavimenti autonomo con navigazione AI.

### 2. Hera Gardener (2 XMR)
Robot per la cura delle piante: irrigazione, potatura, monitoraggio.

### 3. Hera Scheduler (1 XMR)
Sistema di pianificazione e gestione dei robot di servizio.

### 4. Hera Security Robot

Il modulo `security/security_robot.py` orchestra pattugliamento, fusione tra
sensori fisici e risultati del modello di visione, deduplicazione degli allarmi,
notifiche e inoltro a un sistema di sicurezza esistente.

Gli adattatori hardware e AI sono volutamente iniettati: il codice non dichiara
che una telecamera, un modello o un impianto reale siano disponibili quando non
lo sono. `WebhookSecuritySystem` richiede HTTPS (salvo localhost), applica un
timeout e non contiene credenziali hard-coded. Lo stesso adattatore implementa
sia `report_event` sia `notify`, quindi puo essere usato per l'integrazione
dell'impianto o per un canale di notifica webhook.

Esecuzione demo sicura:

```bash
python3 robots/hera/security/security_robot.py
```

Test:

```bash
python3 -m unittest discover -s robots/hera/security -p "test_*.py"
```

## 📦 Tecnologie
- ROS (Robot Operating System)
- Python / C++
- Computer Vision (OpenCV)
- Monero RPC per pagamenti

## 💰 Bounty Attivi
Vedi le issue per i bounty disponibili.
