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
// CHAT DI PYTHO
// ============================================

const pythoResponses = {
    'daniel': [
        '👨‍🌾 Daniel Ioni è il creatore di MyZubster e Pytho! Un visionario che unisce blockchain e natura.',
        '🌟 Daniel ha fondato MyZubster per creare un ecosistema sostenibile dove orti botanici e tecnologia si incontrano.',
        '💚 Daniel crede che la tecnologia possa rendere il mondo più verde e decentralizzato.'
    ],
    'chiesa': [
        '⛪ La chiesa è un punto di riferimento spirituale e comunitario per molti paesi.',
        '🌿 In molte comunità, la chiesa gestisce orti e giardini per sostenere i bisognosi.',
        '🌸 Gli orti della chiesa sono spesso luoghi di pace e riflessione.'
    ],
    'myz': [
        '🪙 MYZ è il token nativo dell\'ecosistema MyZubster, basato su blockchain.',
        '🌿 MYZ serve per incentivare la cura degli orti botanici e la sostenibilità.',
        '💰 Con MYZ puoi pagare servizi, acquistare piante e partecipare alla governance.'
    ],
    'monero': [
        '🔶 Monero (XMR) è una criptovaluta focalizzata sulla privacy e l\'anonimato.',
        '🔒 Le transazioni in Monero sono private e non tracciabili.',
        '🌿 MyZubster accetta pagamenti in Monero per transazioni sicure e private.'
    ],
    'fluffypony': [
        '🐴 Fluffypony è il soprannome di Riccardo Spagni, uno dei fondatori di Monero.',
        '🇮🇹 Riccardo Spagni è italiano e ha portato Monero alla ribalta internazionale.',
        '🛡️ Grazie a Fluffypony, Monero ha mantenuto la sua rotta verso la privacy assoluta.'
    ],
    'musica': [
        '🎵 La musica è l\'anima del mondo vegetale! Le piante reagiscono positivamente alle vibrazioni sonore.',
        '🌿 Gli studi dimostrano che la musica classica favorisce la crescita delle piante.',
        '🎶 Pytho ama la musica! È il sottofondo perfetto per viaggiare nel tempo.'
    ],
    'default': [
        '👽 Non ho capito. Prova a chiedermi di: Daniel, MYZ, Monero, Fluffypony, chiesa, musica, orto, piante, acqua, concime, malattie, compost, clima, potatura o semina!',
        '🌿 Chiedimi qualcosa su MyZubster o sul tuo orto!'
    ]
};

function getPythoResponse(message) {
    const lower = message.toLowerCase();
    let response = 'default';
    
    if (lower.includes('daniel') || lower.includes('ioni') || lower.includes('creatore')) {
        response = 'daniel';
    } else if (lower.includes('chiesa') || lower.includes('parrocchia')) {
        response = 'chiesa';
    } else if (lower.includes('myz') || lower.includes('token')) {
        response = 'myz';
    } else if (lower.includes('monero') || lower.includes('xmr')) {
        response = 'monero';
    } else if (lower.includes('fluffypony') || lower.includes('riccardo') || lower.includes('spagni')) {
        response = 'fluffypony';
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

app.post('/api/pytho/chat', (req, res) => {
    const { message } = req.body;
    
    if (!message) {
        return res.status(400).json({
            success: false,
            error: 'Pytho ha bisogno di un messaggio per risponderti!'
        });
    }
    
    const response = getPythoResponse(message);
    
    temporalMemory.push({
        event: `🗣️ Chat: "${message}" → "${response.substring(0, 50)}..."`,
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
// ROTTE PAGAMENTI MYZ
// ============================================

app.post('/api/myz/payment/create', (req, res) => {
    const { tag_id, amount } = req.body;
    
    if (!tag_id || !amount) {
        return res.status(400).json({
            success: false,
            error: 'tag_id e amount sono obbligatori'
        });
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
        created_at: new Date().toISOString(),
        synced_to_myz: false
    };
    
    payments.push(payment);
    savePayments(payments);
    res.json({ success: true, ...payment });
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

app.post('/api/myz/sync', (req, res) => {
    try {
        const myzPayments = payments.filter(p => 
            p.currency === 'MYZ' && 
            p.status === 'paid' && 
            !p.synced_to_myz
        );
        
        if (myzPayments.length === 0) {
            return res.json({
                success: true,
                message: 'Nessun pagamento MYZ da sincronizzare',
                synced: 0
            });
        }
        
        let syncedCount = 0;
        for (const payment of myzPayments) {
            payment.synced_to_myz = true;
            payment.synced_at = new Date().toISOString();
            syncedCount++;
        }
        
        savePayments(payments);
        
        res.json({
            success: true,
            message: syncedCount + ' pagamenti MYZ sincronizzati',
            synced: syncedCount
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// ROTTE PAGAMENTI XMR
// ============================================

app.post('/api/cardputer/payment/create', (req, res) => {
    const { tag_id, amount } = req.body;
    
    if (!tag_id || !amount) {
        return res.status(400).json({
            success: false,
            error: 'tag_id e amount sono obbligatori'
        });
    }
    
    const payment_id = 'pay_' + Date.now() + Math.random().toString(36).substr(2, 5);
    const address = XMR_WALLET_ADDRESS;
    
    const payment = {
        id: payment_id,
        tag_id: tag_id,
        amount: parseFloat(amount),
        currency: 'XMR',
        address: address,
        status: 'pending',
        created_at: new Date().toISOString()
    };
    
    payments.push(payment);
    savePayments(payments);
    res.json({
        success: true,
        payment_id: payment_id,
        address: address,
        amount: parseFloat(amount),
        tag: tag_id
    });
});

app.get('/api/cardputer/payments', (req, res) => {
    res.json({
        success: true,
        count: payments.length,
        payments: payments
    });
});

// ============================================
// ROTTA: AGGIORNA STATO PAGAMENTO
// ============================================

app.put('/api/cardputer/payment/status/:payment_id', (req, res) => {
    const { payment_id } = req.params;
    const { status } = req.body;

    if (!status || !['pending', 'paid', 'expired'].includes(status)) {
        return res.status(400).json({
            success: false,
            error: 'Status non valido. Usa: pending, paid, expired'
        });
    }

    const payment = payments.find(p => p.id === payment_id);
    if (!payment) {
        return res.status(404).json({
            success: false,
            error: 'Pagamento non trovato'
        });
    }

    payment.status = status;
    payment.updated_at = new Date().toISOString();
    savePayments(payments);

    res.json({
        success: true,
        payment: payment
    });
});

// ============================================
// DASHBOARD
// ============================================

app.get('/api/dashboard', (req, res) => {
    const totalXMR = payments
        .filter(p => p.currency === 'XMR' && p.status === 'paid')
        .reduce((sum, p) => sum + p.amount, 0);
    
    const totalMYZ = payments
        .filter(p => p.currency === 'MYZ' && p.status === 'paid')
        .reduce((sum, p) => sum + (p.net_amount || p.amount), 0);
    
    res.json({
        success: true,
        dashboard: {
            total_payments: payments.length,
            pending: payments.filter(p => p.status === 'pending').length,
            paid: payments.filter(p => p.status === 'paid').length,
            total_xmr: totalXMR,
            total_myz: totalMYZ,
            wallet: {
                myz: MYZ_WALLET,
                xmr: XMR_WALLET
            }
        }
    });
});

// ============================================
// AVVIA SERVER
// ============================================

app.listen(port, () => {
    console.log('🚀 Pytho Temporal su porta ' + port);
    console.log('👽 Macchina del tempo attiva!');
    console.log('🛸 http://localhost:' + port + '/temporal');
    console.log('📊 http://localhost:' + port + '/api/dashboard');
});

// ============================================
// 🌿 BOTANICAL PAST - Recupero Piante dal Passato
// ============================================
app.post('/api/pytho/botanical-past', async (req, res) => {
    try {
        const { location, year, species, register } = req.body;
        
        console.log('🌿 Botanical Past Request:', { location, year, species, register });
        
        // Carica o crea il database delle piante
        const fs = require('fs');
        const dbPath = './plants.json';
        let plants = [];
        
        if (fs.existsSync(dbPath)) {
            plants = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
        }
        
        // Aggiungi le nuove specie
        const newSpecies = species.map(name => ({
            id: `plant_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
            name: name,
            location: location,
            year: year,
            registered: register || true,
            timestamp: new Date().toISOString()
        }));
        
        plants.push(...newSpecies);
        
        // Salva nel database
        fs.writeFileSync(dbPath, JSON.stringify(plants, null, 2));
        
        res.json({
            success: true,
            message: `✅ ${species.length} specie registrate da ${location} (${year})`,
            location: location,
            year: year,
            species: newSpecies,
            total: plants.length,
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('❌ Errore botanical-past:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// 📋 LISTA TUTTE LE SPECIE
// ============================================
app.get('/api/pytho/all-species', async (req, res) => {
    try {
        const fs = require('fs');
        const dbPath = './plants.json';
        
        if (!fs.existsSync(dbPath)) {
            return res.json([]);
        }
        
        const plants = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
        res.json(plants);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================
// 🔍 SPECIE PER ERA
// ============================================
app.get('/api/pytho/species-by-era', async (req, res) => {
    try {
        const { era } = req.query;
        const fs = require('fs');
        const dbPath = './plants.json';
        
        if (!fs.existsSync(dbPath)) {
            return res.json([]);
        }
        
        const plants = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
        const filtered = plants.filter(p => p.year == era);
        res.json(filtered);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================
// 📊 CONTA SPECIE
// ============================================
app.get('/api/pytho/species-count', async (req, res) => {
    try {
        const fs = require('fs');
        const dbPath = './plants.json';
        
        if (!fs.existsSync(dbPath)) {
            return res.json({ total: 0 });
        }
        
        const plants = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
        res.json({ total: plants.length });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});


// ============================================
// 💰 ROUTE PAGAMENTI MANCANTI
// ============================================

// Lista pagamenti
app.get('/api/myz/payments', async (req, res) => {
    try {
        const fs = require('fs');
        const paymentsFile = './payments.json';
        
        if (!fs.existsSync(paymentsFile)) {
            return res.json({ success: true, payments: [], total: 0 });
        }
        
        const payments = JSON.parse(fs.readFileSync(paymentsFile, 'utf8'));
        res.json({
            success: true,
            payments: payments,
            total: payments.length
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Dettaglio wallet
app.get('/api/myz/wallet', async (req, res) => {
    try {
        const wallet = {
            myz: {
                address: "myz_77d6ddd05bf30e8fef178ac1b5b5e112",
                balance: 14876.4,
                currency: "MYZ"
            },
            xmr: {
                address: "xmr_641340aa6aa86029e833a5e5f5fb2b31",
                balance: 0,
                currency: "XMR"
            },
            lastUpdated: new Date().toISOString()
        };
        res.json({
            success: true,
            data: wallet
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Transazioni
app.get('/api/myz/transactions', async (req, res) => {
    try {
        const fs = require('fs');
        const paymentsFile = './payments.json';
        
        if (!fs.existsSync(paymentsFile)) {
            return res.json({ success: true, transactions: [], total: 0 });
        }
        
        const payments = JSON.parse(fs.readFileSync(paymentsFile, 'utf8'));
        const transactions = payments.map(p => ({
            id: p.id,
            type: p.status === 'paid' ? 'credit' : 'pending',
            amount: p.amount,
            currency: p.currency || 'MYZ',
            status: p.status,
            description: `Pagamento da ${p.tag_id || 'utente'}`,
            timestamp: p.created_at || p.createdAt || new Date().toISOString()
        }));
        
        // Ordina per data (più recenti prima)
        transactions.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        res.json({
            success: true,
            transactions: transactions.slice(0, 20),
            total: transactions.length
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Dettaglio pagamento singolo
app.get('/api/myz/payment/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const fs = require('fs');
        const paymentsFile = './payments.json';
        
        if (!fs.existsSync(paymentsFile)) {
            return res.status(404).json({ success: false, error: 'Pagamento non trovato' });
        }
        
        const payments = JSON.parse(fs.readFileSync(paymentsFile, 'utf8'));
        const payment = payments.find(p => p.id === id);
        
        if (!payment) {
            return res.status(404).json({ success: false, error: 'Pagamento non trovato' });
        }
        
        res.json({
            success: true,
            data: payment
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// Sincronizza pagamenti
app.post('/api/myz/sync', async (req, res) => {
    try {
        const fs = require('fs');
        const paymentsFile = './payments.json';
        
        if (!fs.existsSync(paymentsFile)) {
            return res.json({ success: true, message: 'Nessun pagamento da sincronizzare', synced: 0 });
        }
        
        const payments = JSON.parse(fs.readFileSync(paymentsFile, 'utf8'));
        let synced = 0;
        
        payments.forEach(p => {
            if (p.status === 'paid' && !p.synced_to_myz) {
                p.synced_to_myz = true;
                p.synced_at = new Date().toISOString();
                synced++;
            }
        });
        
        fs.writeFileSync(paymentsFile, JSON.stringify(payments, null, 2));
        
        res.json({
            success: true,
            message: `${synced} pagamenti MYZ sincronizzati`,
            synced: synced
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});
