const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

// File di persistenza
const DATA_FILE = path.join(__dirname, 'payments.json');

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
    fs.writeFileSync(DATA_FILE, JSON.stringify(p, null, 2));
}

let payments = loadPayments();

// Memoria temporale di Pytho
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
// RISPOSTE DI PYTHO
// ============================================

const pythoResponses = {
    'myz': [
        '🪙 MYZ è il token nativo dell\'ecosistema MyZubster, basato su blockchain.',
        '🌿 MYZ serve per incentivare la cura degli orti botanici e la sostenibilità.',
        '💰 Con MYZ puoi pagare servizi, acquistare piante e partecipare alla governance.',
        '🌱 Ogni pianta registrata su MyZubster genera ricompense in MYZ.'
    ],
    'monero': [
        '🔶 Monero (XMR) è una criptovaluta focalizzata sulla privacy e l\'anonimato.',
        '🔒 Le transazioni in Monero sono private e non tracciabili.',
        '💰 Monero utilizza firme ad anello e indirizzi stealth per proteggere la privacy.',
        '🌿 MyZubster accetta pagamenti in Monero per transazioni sicure e private.'
    ],
    'fluffypony': [
        '🐴 Fluffypony è il soprannome di Riccardo Spagni, uno dei fondatori di Monero.',
        '🇮🇹 Riccardo Spagni è italiano e ha portato Monero alla ribalta internazionale.',
        '🛡️ Grazie a Fluffypony, Monero ha mantenuto la sua rotta verso la privacy assoluta.',
        '💚 Pytho ammira Fluffypony per la sua dedizione alla privacy e alla libertà.'
    ],
    'chiesa': [
        '⛪ La chiesa è un punto di riferimento spirituale e comunitario.',
        '🌿 In molte comunità, la chiesa gestisce orti e giardini per sostenere i bisognosi.',
        '🌸 Gli orti della chiesa sono spesso luoghi di pace e riflessione.',
        '🌻 La chiesa può essere un partner importante per progetti di giardinaggio comunitario.'
    ],
    'musica': [
        '🎵 La musica è l\'anima del mondo vegetale! Le piante reagiscono positivamente alle vibrazioni sonore.',
        '🌿 Gli studi dimostrano che la musica classica favorisce la crescita delle piante.',
        '🎶 Pytho ama la musica! È il sottofondo perfetto per viaggiare nel tempo.',
        '🌻 La musica e la natura sono due facce della stessa medaglia.'
    ],
    'default': [
        '👽 Non ho capito. Prova a chiedermi di: MYZ, Monero, Fluffypony, chiesa, musica, orto, piante, acqua, concime, malattie, compost, clima, potatura o semina!',
        '🌿 Chiedimi qualcosa su MyZubster o sul tuo orto!'
    ],
    'help': [
        '👽 Ciao! Sono Pytho. Chiedimi di: MYZ, Monero, Fluffypony, chiesa, musica, orto, piante, acqua, concime, malattie, compost, clima, potatura o semina!',
        '🌿 Pytho è un esperto di orti e di MyZubster.'
    ]
};

// Funzione per ottenere risposte
function getPythoResponse(message) {
    const lower = message.toLowerCase();
    let response = 'default';
    
    if (lower.includes('myz') || lower.includes('token')) {
        response = 'myz';
    } else if (lower.includes('monero') || lower.includes('xmr')) {
        response = 'monero';
    } else if (lower.includes('fluffypony') || lower.includes('riccardo')) {
        response = 'fluffypony';
    } else if (lower.includes('chiesa') || lower.includes('parrocchia')) {
        response = 'chiesa';
    } else if (lower.includes('musica') || lower.includes('canzone')) {
        response = 'musica';
    } else if (lower.includes('help') || lower.includes('aiuto')) {
        response = 'help';
    } else if (lower.includes('orto') || lower.includes('giardino')) {
        response = 'orto';
    } else if (lower.includes('pianta') || lower.includes('fiore')) {
        response = 'piante';
    } else if (lower.includes('acqua') || lower.includes('innaffiare')) {
        response = 'acqua';
    } else if (lower.includes('concime') || lower.includes('fertilizzante')) {
        response = 'concime';
    } else if (lower.includes('malattia') || lower.includes('funghi')) {
        response = 'malattie';
    } else if (lower.includes('compost')) {
        response = 'compost';
    } else if (lower.includes('clima') || lower.includes('sole')) {
        response = 'clima';
    } else if (lower.includes('potatura') || lower.includes('taglia')) {
        response = 'potatura';
    } else if (lower.includes('semina') || lower.includes('semi')) {
        response = 'semina';
    }
    
    const responses = pythoResponses[response] || pythoResponses['default'];
    return responses[Math.floor(Math.random() * responses.length)];
}

// ============================================
// ROTTE HTML
// ============================================

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/temporal', (req, res) => {
    res.sendFile(path.join(__dirname, 'pytho-temporal.html'));
});

app.get('/chat', (req, res) => {
    res.sendFile(path.join(__dirname, 'pytho-chat.html'));
});

app.get('/mappa-globale', (req, res) => {
    res.sendFile(path.join(__dirname, 'mappa-globale.html'));
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

// ============================================
// CHAT DI PYTHO (CON NOTIZIE)
// ============================================

// Notizie di esempio
const sampleNews = [
    '📰 **Monero raggiunge nuovo massimo storico!** - La privacy coin cresce del 15% in una settimana.',
    '📰 **Giardino Botanico di Roma inizia progetto di sostenibilità** - Nuovo orto urbano con pagamenti in XMR.',
    '📰 **Fluffypony: "La privacy è un diritto fondamentale"** - Intervista esclusiva al fondatore di Monero.',
    '📰 **MyZubster annuncia partnership con comuni italiani** - Progetto di orti botanici decentralizzati.',
    '📰 **Musica e natura: studio rivela che le piante amano Mozart** - Crescita del 20% con la musica classica.'
];

app.post('/api/pytho/chat', (req, res) => {
    const { message } = req.body;
    
    if (!message) {
        return res.status(400).json({
            success: false,
            error: 'Pytho ha bisogno di un messaggio per risponderti!'
        });
    }
    
    const lower = message.toLowerCase();
    let response = '';
    
    // Verifica se la domanda è sulle notizie
    if (lower.includes('notizie') || lower.includes('news') || lower.includes('ultime') || lower.includes('novità') || lower.includes('aggiornamenti')) {
        // Notizie per Daniel
        if (lower.includes('daniel') || lower.includes('io') || lower.includes('mio')) {
            response = '📰 **Ecco le notizie che potrebbero interessarti, Daniel:**\n\n' + sampleNews.map((n, i) => `${i+1}. ${n}`).join('\n\n');
        } else {
            response = '📰 **Ultime notizie dal mondo:**\n\n' + sampleNews.map((n, i) => `${i+1}. ${n}`).join('\n\n');
        }
    } 
    // Notizie su Monero
    else if (lower.includes('monero') || lower.includes('xmr')) {
        const moneroNews = sampleNews.filter(n => n.toLowerCase().includes('monero') || n.toLowerCase().includes('xmr'));
        if (moneroNews.length > 0) {
            response = '🔶 **Notizie su Monero:**\n\n' + moneroNews.map((n, i) => `${i+1}. ${n}`).join('\n\n');
        } else {
            response = getPythoResponse(message);
        }
    }
    // Notizie sugli orti
    else if (lower.includes('giardino') || lower.includes('orto') || lower.includes('botanico')) {
        const gardenNews = sampleNews.filter(n => n.toLowerCase().includes('giardino') || n.toLowerCase().includes('orto') || n.toLowerCase().includes('botanico'));
        if (gardenNews.length > 0) {
            response = '🌿 **Notizie sui giardini botanici:**\n\n' + gardenNews.map((n, i) => `${i+1}. ${n}`).join('\n\n');
        } else {
            response = getPythoResponse(message);
        }
    }
    // Altrimenti risposta standard
    else {
        response = getPythoResponse(message);
    }
    
    temporalMemory.push({
        event: `🗣️ Chat: "${message}" → "${response.substring(0, 100)}..."`,
        timestamp: new Date().toISOString()
    });
    
    res.json({
        success: true,
        message: message,
        response: response,
        pytho_says: response,
        timestamp: new Date().toISOString()
    });
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
    "Salvia Romana": { status: "🌱 In riproduzione", progress: 0, era: "1500", location: "Orto Botanico di Roma" }
};

app.post('/api/pytho/reproduce/:species', (req, res) => {
    const { species } = req.params;
    if (reproductionStatus[species]) {
        reproductionStatus[species].status = "🌱 In riproduzione";
        reproductionStatus[species].progress = Math.floor(Math.random() * 100) + 1;
        res.json({ success: true, species, status: reproductionStatus[species], pytho_says: `🌿 La ${species} è in riproduzione!` });
    } else {
        res.status(404).json({ success: false, error: `Specie ${species} non trovata` });
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

// Avvia il server
app.listen(port, () => {
    console.log('🚀 Pytho Temporal su porta ' + port);
    console.log('👽 Macchina del tempo attiva!');
    console.log('🛸 http://localhost:' + port + '/temporal');
    console.log('📊 http://localhost:' + port + '/api/dashboard');
});
