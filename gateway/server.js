const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3004;

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
// CHAT DI PYTHO - INTEGRAZIONE AI & RISPOSTE RICCHE
// ============================================

const { pythoResponses } = require('./pytho-responses.js');
const { getPythoAIResponse } = require('./pytho-ai.js');

function getPythoResponse(message) {
    const lower = message.toLowerCase();
    let key = 'default';
    
    // Mappatura chiavi per risposte predefinite
    const keywords = {
        'daniel': ['daniel', 'ioni'],
        'chiesa': ['chiesa', 'parrocchia', 'fede', 'monastero', 'comunità'],
        'myz': ['myz', 'token'],
        'monero': ['monero', 'xmr', 'privacy', 'mining', 'storia_monero'],
        'fluffypony': ['fluffypony', 'riccardo', 'spagni'],
        'musica': ['musica', 'canzone', 'strumenti', 'canto', 'natura_musica'],
        'pomodori': ['pomodori'],
        'orto': ['orto', 'giardino'],
        'piante': ['pianta', 'fiore'],
        'acqua': ['acqua', 'innaffiare'],
        'concime': ['concime', 'fertilizzante'],
        'malattie': ['malattia', 'funghi', 'insetti'],
        'compost': ['compost'],
        'clima': ['clima', 'sole', 'gelo'],
        'potatura': ['potatura', 'taglia'],
        'semina': ['semina', 'semi'],
        'help': ['help', 'aiuto']
    };

    for (const [k, words] of Object.entries(keywords)) {
        if (words.some(w => lower.includes(w))) {
            key = k;
            break;
        }
    }
    
    const responses = pythoResponses[key] || pythoResponses['default'];
    return responses[Math.floor(Math.random() * responses.length)];
}

app.post('/api/pytho/chat', async (req, res) => {
    const { message, history } = req.body;
    
    if (!message) {
        return res.status(400).json({
            success: false,
            error: 'Pytho ha bisogno di un messaggio per risponderti!'
        });
    }
    
    // Prova con l'AI (Ollama), altrimenti usa le risposte predefinite
    let response;
    try {
        response = await getPythoAIResponse(message, history || []);
    } catch (e) {
        console.error('Errore AI, uso fallback:', e);
        response = getPythoResponse(message);
    }
    
    // Se l'AI restituisce null o vuoto, usa fallback
    if (!response) {
        response = getPythoResponse(message);
    }
    
    temporalMemory.push({
        event: `🗣️ Chat: "${message}"`,
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

// Avvia il server
app.listen(port, () => {
    console.log('🚀 Pytho Temporal su porta ' + port);
    console.log('👽 Macchina del tempo attiva!');
    console.log('🛸 http://localhost:' + port + '/temporal');
    console.log('📊 http://localhost:' + port + '/api/dashboard');
});

// ============================================
// 📡 ROTTE NFC
// ============================================
const nfcRoutes = require('./nfc/nfc.routes');
app.use('/api/nfc', nfcRoutes);

console.log('📡 NFC API attiva!');
