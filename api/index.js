const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Percorsi corretti per Vercel
const BASE_DIR = path.join(__dirname, '..');
const GATEWAY_DIR = path.join(BASE_DIR, 'gateway');
const DATA_FILE = path.join(GATEWAY_DIR, 'payments.json');

// Configurazione wallet
const MYZ_WALLET = 'myz_77d6ddd05bf30e8fef178ac1b5b5e112';
const XMR_WALLET = 'xmr_641340aa6aa86029e833a5e5f5fb2b31';
const PLATFORM_FEE = 2;

// Carica pagamenti
function loadPayments() {
    try {
        if (fs.existsSync(DATA_FILE)) {
            return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
        }
    } catch (e) {}
    return [];
}

function savePayments(p) {
    try {
        fs.writeFileSync(DATA_FILE, JSON.stringify(p, null, 2));
    } catch (e) {}
}

let payments = loadPayments();

// ============================================
// MEMORIA TEMPORALE DI PYTHO
// ============================================

const temporalMemory = [];
const timelineEvents = [
    { event: '👽 Pytho creato', year: '2024', status: '✅' },
    { event: '🌿 Primo orto botanico', year: '2024', status: '✅' },
    { event: '🏛️ Comune di Firenze', year: '2024', status: '✅' },
    { event: '🚀 Gateway live', year: '2024', status: '✅' },
    { event: '🛸 Pytho viaggia nel tempo', year: '2124', status: '⏳' },
    { event: '🌌 Pytho diventa leggenda', year: '3000', status: '🌀' }
];

// ============================================
// ROTTE HTML
// ============================================

app.get('/', (req, res) => {
    res.sendFile(path.join(GATEWAY_DIR, 'index.html'));
});

app.get('/temporal', (req, res) => {
    res.sendFile(path.join(GATEWAY_DIR, 'pytho-temporal.html'));
});

app.get('/temporal.css', (req, res) => {
    res.sendFile(path.join(GATEWAY_DIR, 'temporal.css'));
});

app.get('/temporal.js', (req, res) => {
    res.sendFile(path.join(GATEWAY_DIR, 'temporal.js'));
});

app.get('/mappa-globale', (req, res) => {
    res.sendFile(path.join(GATEWAY_DIR, 'mappa-globale.html'));
});

// ============================================
// ROTTE PYTHO TEMPORAL
// ============================================

app.post('/api/pytho/timetravel', (req, res) => {
    const { destination, year } = req.body;
    const result = {
        timestamp: new Date().toISOString(),
        destination: destination || 'Orto Botanico di Roma',
        year: year || 2024,
        status: '🛸 Viaggio completato!',
        pytho: '👽 Il tempo è un concetto umano...',
        flux: '1.21 GW ⚡'
    };
    temporalMemory.push({ event: `Viaggio al ${destination} (${year})`, timestamp: new Date().toISOString() });
    res.json({ success: true, travel: result });
});

app.get('/api/pytho/timeline', (req, res) => {
    res.json({
        success: true,
        timeline: timelineEvents,
        temporal_memory: temporalMemory,
        status: '🟢 Attivo'
    });
});

app.get('/api/pytho/flux', (req, res) => {
    res.json({
        success: true,
        flux: {
            power: '1.21 GW',
            charge: Math.floor(Math.random() * 100) + 1 + '%',
            status: '🔋 Carico'
        }
    });
});

app.post('/api/pytho/voice', (req, res) => {
    const { command } = req.body;
    if (!command) {
        return res.status(400).json({ success: false, error: 'Nessun comando vocale ricevuto' });
    }
    const yearMatch = command.match(/\b(\d{4})\b/);
    const destMatch = command.match(/(?:destinazione|a|al|nel)\s+([a-zA-Z\s]+)/i);
    let response = { success: true, command: command, pytho_says: '👽 Comando ricevuto!', action: null };
    if (yearMatch) {
        const year = yearMatch[1];
        const destination = destMatch ? destMatch[1].trim() : 'Orto Botanico di Roma';
        response.pytho_says = `🛸 Viaggio al ${destination} nel ${year} in corso...`;
        response.action = 'timetravel';
        response.year = year;
        response.destination = destination;
        temporalMemory.push({
            event: `🗣️ Comando vocale: "${command}" → ${destination} (${year})`,
            timestamp: new Date().toISOString()
        });
        res.json({ ...response, travel: { destination, year: parseInt(year), status: '✅ Viaggio vocale completato!', flux: '1.21 GW ⚡' } });
    } else {
        response.pytho_says = "👽 Non ho capito l'anno. Prova: 'Pytho, viaggia al 2124 a Firenze'";
        res.json(response);
    }
});

// ============================================
// ROTTE PAGAMENTI
// ============================================

app.post('/api/myz/payment/create', (req, res) => {
    const { tag_id, amount } = req.body;
    if (!tag_id || !amount) {
        return res.status(400).json({ success: false, error: 'tag_id e amount sono obbligatori' });
    }
    const fee = (parseFloat(amount) * PLATFORM_FEE) / 100;
    const netAmount = parseFloat(amount) - fee;
    const payment = {
        id: 'myz_' + Date.now() + Math.random().toString(36).substr(2, 5),
        tag_id,
        amount: parseFloat(amount),
        currency: 'MYZ',
        address: MYZ_WALLET,
        fee: fee,
        net_amount: netAmount,
        status: 'pending',
        created_at: new Date().toISOString()
    };
    payments.push(payment);
    savePayments(payments);
    res.json({ success: true, ...payment });
});

app.get('/api/dashboard', (req, res) => {
    const total = payments.reduce((s, p) => s + (p.net_amount || p.amount), 0);
    res.json({
        success: true,
        dashboard: {
            total_payments: payments.length,
            pending: payments.filter(p => p.status === 'pending').length,
            paid: payments.filter(p => p.status === 'paid').length,
            total_myz: total,
            wallet: { myz: MYZ_WALLET, xmr: XMR_WALLET }
        }
    });
});

app.get('/api/cardputer/payments', (req, res) => {
    res.json({ success: true, count: payments.length, payments: payments });
});

app.get('/api/myz/stats', (req, res) => {
    const myzPayments = payments.filter(p => p.currency === 'MYZ');
    const totalMYZ = myzPayments.reduce((sum, p) => sum + (p.net_amount || p.amount), 0);
    const totalFee = myzPayments.reduce((sum, p) => sum + (p.fee || 0), 0);
    res.json({
        success: true,
        stats: {
            total_payments: myzPayments.length,
            total_amount: totalMYZ,
            total_fee: totalFee,
            pending: myzPayments.filter(p => p.status === 'pending').length,
            paid: myzPayments.filter(p => p.status === 'paid').length,
            synced: myzPayments.filter(p => p.synced_to_myz).length
        }
    });
});

// ============================================
// MAPPA GLOBALE
// ============================================

const globalMap = {
    "1500": {
        "Orto Botanico di Roma": {
            coordinates: [41.9028, 12.4964],
            species: ["Rosa Antica", "Lilio", "Orchidea Selvatica", "Menta Romana", "Basilico Antico", "Salvia Romana"],
            era: "Rinascimento",
            status: "🌿 Recuperato"
        }
    },
    "1800": {
        "Orto Botanico di Napoli": {
            coordinates: [40.8518, 14.2681],
            species: ["Lilio di Napoli", "Orchidea Napoletana", "Gelsomino Antico", "Violette del Vesuvio"],
            era: "Ottocento",
            status: "🌿 Recuperato"
        }
    },
    "1900": {
        "Orto Botanico di Palermo": {
            coordinates: [38.1157, 13.3615],
            species: ["Orchidea Siciliana", "Lilio di Sicilia", "Rosa Palermitana"],
            era: "Novecento",
            status: "🌿 Recuperato"
        }
    },
    "2024": {
        "Orto Botanico di Roma": {
            coordinates: [41.9028, 12.4964],
            species: ["Rosa Moderna", "Lilio Ibrido", "Orchidea Tropicale"],
            era: "Presente",
            status: "🌱 Attivo"
        }
    },
    "2124": {
        "Giardino del Futuro": {
            coordinates: [45.4642, 9.1900],
            species: ["Rosa Quantica", "Lilio Stellare", "Orchidea Temporale", "Albero di Luce"],
            era: "Futuro",
            status: "🛸 Scoperto"
        }
    },
    "3000": {
        "Orto Botanico Galattico": {
            coordinates: [0, 0],
            species: ["Rosa Galattica", "Lilio Interstellare", "Orchidea Quantica", "Fiori di Nebulosa"],
            era: "Galattico",
            status: "🌌 Esplorato"
        }
    }
};

app.get('/api/pytho/global-map', (req, res) => {
    res.json({
        success: true,
        map: globalMap,
        total_locations: Object.keys(globalMap).length,
        pytho_message: "🌍 La mappa globale del passato è pronta!"
    });
});

app.get('/api/pytho/search-plant/:name', (req, res) => {
    const { name } = req.params;
    const results = [];
    for (const [year, locations] of Object.entries(globalMap)) {
        for (const [location, data] of Object.entries(locations)) {
            const found = data.species.filter(s => s.toLowerCase().includes(name.toLowerCase()));
            if (found.length > 0) {
                results.push({ year, location, species: found, era: data.era, coordinates: data.coordinates });
            }
        }
    }
    if (results.length > 0) {
        res.json({
            success: true,
            plant: name,
            found: results,
            total: results.length,
            pytho_says: `👽 Ho trovato ${results.length} corrispondenze per "${name}"!`
        });
    } else {
        res.json({
            success: false,
            plant: name,
            found: [],
            pytho_says: `🌿 Non ho trovato "${name}" nella mappa globale...`
        });
    }
});

// ============================================
// RIPRODUZIONE SPECIE
// ============================================

const reproductionStatus = {
    "Rosa Antica": { status: "🌱 In riproduzione", progress: 0, era: "1500", location: "Orto Botanico di Roma" },
    "Lilio": { status: "🌱 In riproduzione", progress: 0, era: "1500", location: "Orto Botanico di Roma" },
    "Orchidea Selvatica": { status: "🌱 In riproduzione", progress: 0, era: "1500", location: "Orto Botanico di Roma" },
    "Menta Romana": { status: "🌱 In riproduzione", progress: 0, era: "1500", location: "Orto Botanico di Roma" },
    "Basilico Antico": { status: "🌱 In riproduzione", progress: 0, era: "1500", location: "Orto Botanico di Roma" },
    "Salvia Romana": { status: "🌱 In riproduzione", progress: 0, era: "1500", location: "Orto Botanico di Roma" },
    "Lilio di Napoli": { status: "🌱 In riproduzione", progress: 0, era: "1800", location: "Orto Botanico di Napoli" },
    "Orchidea Napoletana": { status: "🌱 In riproduzione", progress: 0, era: "1800", location: "Orto Botanico di Napoli" },
    "Gelsomino Antico": { status: "🌱 In riproduzione", progress: 0, era: "1800", location: "Orto Botanico di Napoli" },
    "Violette del Vesuvio": { status: "🌱 In riproduzione", progress: 0, era: "1800", location: "Orto Botanico di Napoli" },
    "Orchidea Siciliana": { status: "🌱 In riproduzione", progress: 0, era: "1900", location: "Orto Botanico di Palermo" },
    "Lilio di Sicilia": { status: "🌱 In riproduzione", progress: 0, era: "1900", location: "Orto Botanico di Palermo" },
    "Rosa Palermitana": { status: "🌱 In riproduzione", progress: 0, era: "1900", location: "Orto Botanico di Palermo" },
    "Rosa Quantica": { status: "🛸 In sviluppo", progress: 0, era: "2124", location: "Giardino del Futuro" },
    "Lilio Stellare": { status: "🛸 In sviluppo", progress: 0, era: "2124", location: "Giardino del Futuro" },
    "Orchidea Temporale": { status: "🛸 In sviluppo", progress: 0, era: "2124", location: "Giardino del Futuro" },
    "Albero di Luce": { status: "🛸 In sviluppo", progress: 0, era: "2124", location: "Giardino del Futuro" },
    "Rosa Galattica": { status: "🌌 In esplorazione", progress: 0, era: "3000", location: "Orto Botanico Galattico" },
    "Lilio Interstellare": { status: "🌌 In esplorazione", progress: 0, era: "3000", location: "Orto Botanico Galattico" },
    "Orchidea Quantica": { status: "🌌 In esplorazione", progress: 0, era: "3000", location: "Orto Botanico Galattico" },
    "Fiori di Nebulosa": { status: "🌌 In esplorazione", progress: 0, era: "3000", location: "Orto Botanico Galattico" }
};

app.post('/api/pytho/reproduce/:species', (req, res) => {
    const { species } = req.params;
    if (reproductionStatus[species]) {
        reproductionStatus[species].status = "🌱 In riproduzione";
        reproductionStatus[species].progress = Math.floor(Math.random() * 100) + 1;
        res.json({ success: true, species, status: reproductionStatus[species], pytho_says: `🌿 La ${species} è in riproduzione!` });
    } else {
        res.status(404).json({ success: false, error: `Specie ${species} non trovata`, available_species: Object.keys(reproductionStatus) });
    }
});

app.get('/api/pytho/reproduction-status', (req, res) => {
    const total = Object.keys(reproductionStatus).length;
    const completed = Object.values(reproductionStatus).filter(s => s.progress >= 100).length;
    const inProgress = Object.values(reproductionStatus).filter(s => s.progress > 0 && s.progress < 100).length;
    res.json({
        success: true,
        total_species: total,
        completed: completed,
        in_progress: inProgress,
        details: reproductionStatus,
        pytho_says: `🌿 ${completed}/${total} specie riprodotte!`
    });
});

app.post('/api/pytho/complete-reproduction/:species', (req, res) => {
    const { species } = req.params;
    if (reproductionStatus[species]) {
        reproductionStatus[species].status = "✅ Riprodotta!";
        reproductionStatus[species].progress = 100;
        temporalMemory.push({
            event: `🌿 Specie riprodotta: ${species}`,
            timestamp: new Date().toISOString()
        });
        res.json({
            success: true,
            species,
            status: reproductionStatus[species],
            pytho_says: `🎉 La ${species} è stata riprodotta con successo!`
        });
    } else {
        res.status(404).json({ success: false, error: `Specie ${species} non trovata` });
    }
});

// Avvia server
app.listen(port, () => {
    console.log('🚀 Pytho Temporal su porta ' + port);
    console.log('👽 Macchina del tempo attiva!');
    console.log('🛸 http://localhost:' + port + '/temporal');
    console.log('📊 http://localhost:' + port + '/api/dashboard');
});

module.exports = app;
