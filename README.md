# 👽 Pytho Temporal - MyZubster Gateway

## 🌿 La Macchina del Tempo Open Source

Pytho Temporal è un gateway decentralizzato che unisce **orti botanici**, **blockchain** e **intelligenza artificiale** per creare un ecosistema sostenibile e innovativo.

---

## 🚀 Funzionalità

### 🤖 Pytho Chat - Assistente AI
Pytho è un chatbot intelligente che risponde a domande su:
- 🌱 **Orto e giardinaggio** - Consigli su coltivazione, piante, concime e malattie
- 🪙 **MYZ Token** - Informazioni sul token nativo di MyZubster
- 🔶 **Monero (XMR)** - Storia, privacy e funzionamento di Monero
- 🐴 **Fluffypony** - Storia di Riccardo Spagni e il suo ruolo in Monero
- ⛪ **Chiesa e comunità** - Il ruolo della chiesa negli orti botanici
- 🎵 **Musica e natura** - Come la musica influenza la crescita delle piante
- 📰 **Notizie in tempo reale** - Aggiornamenti su Monero, blockchain e giardini botanici

### ⏳ Macchina del Tempo
Viaggia attraverso le epoche e registra orti botanici dal passato al futuro:
- **1500** - Orto Botanico di Roma (Rinascimento)
- **1800** - Orto Botanico di Napoli (Ottocento)
- **1900** - Orto Botanico di Palermo (Novecento)
- **2024** - Orto Botanico di Roma (Presente)
- **2124** - Giardino del Futuro (Futuro)
- **3000** - Orto Botanico Galattico (Epoca Galattica)

### 🌍 Mappa Globale del Passato
Esplora le 24 specie vegetali recuperate in 6 epoche diverse, con coordinate geografiche e dettagli storici.

### 💰 Pagamenti Decentralizzati
- **Monero (XMR)** - Pagamenti privati e sicuri
- **MYZ Token** - Token nativo dell'ecosistema MyZubster
- **Platform Fee** - 2% su ogni transazione

### 🌿 24 Specie Recuperate

#### 1500 - Rinascimento (6 specie)
- Rosa Antica, Lilio, Orchidea Selvatica, Menta Romana, Basilico Antico, Salvia Romana

#### 1800 - Ottocento (4 specie)
- Lilio di Napoli, Orchidea Napoletana, Gelsomino Antico, Violette del Vesuvio

#### 1900 - Novecento (3 specie)
- Orchidea Siciliana, Lilio di Sicilia, Rosa Palermitana

#### 2024 - Presente (3 specie)
- Rosa Moderna, Lilio Ibrido, Orchidea Tropicale

#### 2124 - Futuro (4 specie)
- Rosa Quantica, Lilio Stellare, Orchidea Temporale, Albero di Luce

#### 3000 - Epoca Galattica (4 specie)
- Rosa Galattica, Lilio Interstellare, Orchidea Quantica, Fiori di Nebulosa

---

## 🛠️ Tecnologie Utilizzate

```yaml
Backend:
  - Node.js (v18+)
  - Express.js
  - PM2 (Process Manager)

Blockchain:
  - Monero (XMR) - Privacy-first
  - MyZubster Token (MYZ)

Infrastruttura:
  - VPS Ubuntu 24.04
  - Cloudflare DNS
  - Vercel (Deploy)
  - GitHub (Versioning)

Frontend:
  - HTML + CSS
  - JavaScript Vanilla
  - CSS Animazioni
```

## 📦 Installazione

```bash
# Clona il repository
git clone https://github.com/DanielIoni-creator/I-ECO-01.git
cd I-ECO-01/gateway

# Installa le dipendenze
npm install

# Avvia il gateway
node server.js
```

## 🔧 Configurazione

### Variabili d'Ambiente

Crea un file `.env` nella root del progetto:

```env
MYZUBSTER_WALLET_ADDRESS=myz_77d6ddd05bf30e8fef178ac1b5b5e112
MYZUBSTER_XMR_WALLET_ADDRESS=xmr_641340aa6aa86029e833a5e5f5fb2b31
PLATFORM_FEE=2
NODE_ENV=production
```

### Deploy su Vercel

```bash
# Installa Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

## 📡 API Endpoints

### Pytho Chat

```bash
POST /api/pytho/chat
{
  "message": "Cosa sono gli MYZ?"
}
```

### Macchina del Tempo

```bash
POST /api/pytho/timetravel
{
  "destination": "Orto Botanico di Roma",
  "year": 1500
}
```

### Dashboard

```bash
GET /api/dashboard
```

### Mappa Globale

```bash
GET /api/pytho/global-map
GET /api/pytho/search-plant/:name
```

### Pagamenti

```bash
POST /api/myz/payment/create
{
  "tag_id": "TEST-001",
  "amount": 10
}
```

### Riproduzione Specie

```bash
POST /api/pytho/reproduce/:species
POST /api/pytho/complete-reproduction/:species
GET /api/pytho/reproduction-status
```

## 🌐 URL Live

| Servizio | URL | Stato |
|---|---|---|
| Sito | https://myzubster-gateway.vercel.app | ✅ Live |
| Chat Pytho | https://myzubster-gateway.vercel.app/chat | ✅ Live |
| Macchina del Tempo | https://myzubster-gateway.vercel.app/temporal | ✅ Live |
| Mappa Globale | https://myzubster-gateway.vercel.app/mappa-globale | ✅ Live |
| Dashboard | https://myzubster-gateway.vercel.app/api/dashboard | ✅ Live |

## 👽 La Storia di Pytho

Pytho è l'alieno guardiano dell'ecosistema MyZubster. La sua missione è:

- Proteggere gli orti botanici nel tempo e nello spazio
- Registrare le specie vegetali su blockchain
- Guidare gli utenti con consigli intelligenti
- Connettere passato, presente e futuro attraverso la tecnologia

### Il Manifesto di Pytho

```text
👽 No capi, solo codice
🛸 Pagamenti decentralizzati
💚 Open source per tutti
🚀 Innovazione sostenibile
🌿 Orti botanici su blockchain
🏛️ Comuni partecipativi
```

---

## 🌐 TAZ MyZubster — Stato documentato

### ✅ Metaverse TAZ — COMPLETATA

La **TAZ MyZubster nel metaverso è già avvenuta ed è considerata completata** nella storia/documentazione del progetto, con **Daniel Ioni, i suoi amici e Fluffypony**.

In questa fase, **Fluffypony** è rappresentato come robot barista e performer del TAZ environment, con capacità di servizio, danza/intrattenimento, **proiezioni laser/video** e **crittografia visiva**.

Questa esperienza costituisce il precedente digitale della roadmap TAZ e documenta che il concept è già stato sperimentato nel mondo virtuale.

### ⏳ Riccione Real-World TAZ — DA REALIZZARE

La **TAZ fisica a Riccione** resta un progetto separato e ancora da completare. Il pilot reale richiede coordinamento con il territorio, spazio fisico, attività dal vivo e verifica dei deliverable associati.

Issue di riferimento: **#40 — MyZubster TAZ DAY - Riccione (Fase 1)**.

### 💰 Stato bounty TAZ

La Metaverse TAZ completata è una **evidenza storica e progettuale**, ma **non determina automaticamente il pagamento o la chiusura delle bounty XMR del pilot reale**. Ogni bounty collegata deve essere verificata rispetto ai propri criteri di accettazione, funding e settlement.

---

## 📰 External Mentions & Discovery

La presenza pubblica di MyZubster sta iniziando a essere intercettata anche da canali esterni e strumenti di discovery dedicati agli sviluppatori.

- **KMP Weekly** — ha indicizzato il contenuto **“NFC Payments in MyZubster: A Complete Guide”**, portando MyZubster all'interno di una community tecnica focalizzata su Kotlin Multiplatform / Compose.
- **Open Issue Map** — sta indicizzando issue pubbliche di **MyZubster-Ecosystem/MyZubsterGateway**, incluse attività come **Security audit checklist for the gateway** e **Collaborative verification system for mapping data**.

Queste indicizzazioni sono utili perché aumentano la discoverability del progetto fuori dai canali proprietari e rendono ancora più importante mantenere **issue, reward, stato dei task, criteri di accettazione e documentazione** chiari e aggiornati.

> Nota: queste citazioni rappresentano discovery/indicizzazione esterna osservata e non endorsement formale del progetto.

---

## 🤝 Contribuire

- Fork il repository
- Crea un branch per la tua feature
- Commit le tue modifiche
- Push sul branch
- Apri una Pull Request

### Issue Aperte

- [#153] - 🌐 Creare index.html responsive per tutti i dispositivi
- [#154] - ⚡ Ottimizzare performance della index
- [#155] - ♿ Accessibilità per tutti gli utenti
- [#156] - ♿ Accessibilità per tutti gli utenti
- [#157] - ♿ Accessibilità per tutti gli utenti
- [#158] - 🌙 Dark Mode e temi personalizzabili
- [#159] - 🆕 Creare nuova index.html completa
- [#160] - 🧪 Test della index su tutte le piattaforme

## 📄 Licenza

MIT License - see LICENSE file for details.

## 🙏 Ringraziamenti

- Monero Community - Per la privacy e la libertà digitale
- Fluffypony - Per la visione e la dedizione
- MyZubster Community - Per il supporto e i contributi

👽 Pytho Temporal: Il tempo è un concetto umano... ma gli orti botanici sono eterni.

Tags: #monero #nodejs #blockchain #opensource #gardening #timetravel #myzubster
