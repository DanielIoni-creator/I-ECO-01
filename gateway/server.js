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
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/temporal', (req, res) => {
    res.sendFile(path.join(__dirname, 'pytho-temporal.html'));
});

app.get('/temporal.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'temporal.css'));
});

app.get('/temporal.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'temporal.js'));
});

// ============================================
// ROTTE PYTHO TEMPORAL
// ============================================

// ROTTA: Viaggia nel tempo
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

// ROTTA: Timeline di Pytho
app.get('/api/pytho/timeline', (req, res) => {
    res.json({
        success: true,
        timeline: timelineEvents,
        temporal_memory: temporalMemory,
        status: '🟢 Attivo'
    });
});

// ROTTA: Flux Capacitor
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

// ROTTA: Riconoscimento vocale - VERSIONE CORRETTA
app.post('/api/pytho/voice', (req, res) => {
    const { command } = req.body;
    
    if (!command) {
        return res.status(400).json({
            success: false,
            error: 'Nessun comando vocale ricevuto'
        });
    }
    
    // Estrai anno (4 cifre)
    const yearMatch = command.match(/\b(\d{4})\b/);
    // Estrai destinazione (parole dopo "destinazione", "a", "al", "nel")
    const destMatch = command.match(/(?:destinazione|a|al|nel)\s+([a-zA-Z\s]+)/i);
    
    let response = {
        success: true,
        command: command,
        pytho_says: '👽 Comando ricevuto!',
        action: null
    };
    
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
        
        res.json({
            ...response,
            travel: {
                destination: destination,
                year: parseInt(year),
                status: '✅ Viaggio vocale completato!',
                flux: '1.21 GW ⚡'
            }
        });
    } else {
        response.pytho_says = "👽 Non ho capito l'anno. Prova: 'Pytho, viaggia al 2124 a Firenze'";
        res.json(response);
    }
});

// ============================================
// ROTTE PAGAMENTI
// ============================================

// ROTTA: Crea pagamento MYZ
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
        created_at: new Date().toISOString()
    };
    
    payments.push(payment);
    savePayments(payments);
    res.json({ success: true, ...payment });
});

// ROTTA: Dashboard
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

// ROTTA: Lista pagamenti
app.get('/api/cardputer/payments', (req, res) => {
    res.json({
        success: true,
        count: payments.length,
        payments: payments
    });
});

// ROTTA: Statistiche MYZ
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
// AVVIA SERVER
// ============================================

app.listen(port, () => {
    console.log('🚀 Pytho Temporal su porta ' + port);
    console.log('👽 Macchina del tempo attiva!');
    console.log('🛸 http://localhost:' + port + '/temporal');
    console.log('📊 http://localhost:' + port + '/api/dashboard');
});
