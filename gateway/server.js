const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3000;

// Configurazione CORS per il dominio
const corsOptions = {
    origin: [
        'http://localhost:3000',
        'http://localhost',
        'http://myzubster.com',
        'http://www.myzubster.com',
        'https://myzubster.com',
        'https://www.myzubster.com',
        'http://209.227.239.219'
    ],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
    credentials: true
};
app.use(cors(corsOptions));

app.use(express.json());

// Servi la pagina index.html per la root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// File di persistenza
const DATA_FILE = path.join(__dirname, 'payments.json');

// Configurazione wallet
const MYZ_WALLET_ADDRESS = process.env.MYZUBSTER_WALLET_ADDRESS || 'myz_77d6ddd05bf30e8fef178ac1b5b5e112';
const XMR_WALLET_ADDRESS = process.env.MYZUBSTER_XMR_WALLET_ADDRESS || 'xmr_641340aa6aa86029e833a5e5f5fb2b31';
const PLATFORM_FEE = parseFloat(process.env.PLATFORM_FEE) || 2;

// Carica dati salvati
function loadPayments() {
    try {
        if (fs.existsSync(DATA_FILE)) {
            const data = fs.readFileSync(DATA_FILE, 'utf8');
            return JSON.parse(data);
        }
    } catch (error) {
        console.error('Errore nel caricamento dati:', error);
    }
    return [];
}

// Salva dati
function savePayments(payments) {
    try {
        fs.writeFileSync(DATA_FILE, JSON.stringify(payments, null, 2));
    } catch (error) {
        console.error('Errore nel salvataggio dati:', error);
    }
}

// Inizializza pagamenti
let payments = loadPayments();

// ============================================
// ROTTE XMR (Monero)
// ============================================

// ROTTA: Crea nuovo pagamento XMR
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

    const newPayment = {
        id: payment_id,
        tag_id: tag_id,
        amount: parseFloat(amount),
        currency: 'XMR',
        address: address,
        status: 'pending',
        created_at: new Date().toISOString()
    };

    payments.push(newPayment);
    savePayments(payments);

    res.json({
        success: true,
        payment_id: payment_id,
        address: address,
        amount: parseFloat(amount),
        qr_code: 'monero:' + address + '?amount=' + amount,
        tag: tag_id
    });
});

// ROTTA: Lista tutti i pagamenti
app.get('/api/cardputer/payments', (req, res) => {
    res.json({
        success: true,
        count: payments.length,
        payments: payments
    });
});

// ROTTA: Aggiorna stato pagamento
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

// ROTTA: Ottieni pagamento specifico
app.get('/api/cardputer/payment/:payment_id', (req, res) => {
    const { payment_id } = req.params;
    const payment = payments.find(p => p.id === payment_id);

    if (!payment) {
        return res.status(404).json({
            success: false,
            error: 'Pagamento non trovato'
        });
    }

    res.json({
        success: true,
        payment: payment
    });
});

// ROTTA: Elimina pagamento
app.delete('/api/cardputer/payment/:payment_id', (req, res) => {
    const { payment_id } = req.params;
    const index = payments.findIndex(p => p.id === payment_id);

    if (index === -1) {
        return res.status(404).json({
            success: false,
            error: 'Pagamento non trovato'
        });
    }

    payments.splice(index, 1);
    savePayments(payments);

    res.json({
        success: true,
        message: 'Pagamento eliminato'
    });
});

// ROTTA: Recupera pagamenti per tag
app.get('/api/cardputer/payments/tag/:tag_id', (req, res) => {
    const { tag_id } = req.params;
    const filtered = payments.filter(p => p.tag_id === tag_id);

    res.json({
        success: true,
        count: filtered.length,
        payments: filtered
    });
});

// ============================================
// ROTTE MYZ (MyZubster)
// ============================================

// ROTTA: Crea pagamento MYZ
app.post('/api/myz/payment/create', (req, res) => {
    const { tag_id, amount, currency } = req.body;
    const curr = currency || 'MYZ';

    if (!tag_id || !amount) {
        return res.status(400).json({
            success: false,
            error: 'tag_id e amount sono obbligatori'
        });
    }

    const payment_id = 'myz_' + Date.now() + Math.random().toString(36).substr(2, 5);
    const address = curr === 'XMR' ? XMR_WALLET_ADDRESS : MYZ_WALLET_ADDRESS;
    
    const fee = (parseFloat(amount) * PLATFORM_FEE) / 100;
    const netAmount = parseFloat(amount) - fee;

    const newPayment = {
        id: payment_id,
        tag_id: tag_id,
        amount: parseFloat(amount),
        currency: curr,
        address: address,
        fee: fee,
        net_amount: netAmount,
        status: 'pending',
        created_at: new Date().toISOString(),
        synced_to_myz: false
    };

    payments.push(newPayment);
    savePayments(payments);

    res.json({
        success: true,
        payment_id: payment_id,
        address: address,
        amount: parseFloat(amount),
        currency: curr,
        fee: fee,
        net_amount: netAmount,
        qr_code: curr.toLowerCase() + ':' + address + '?amount=' + amount,
        tag: tag_id
    });
});

// ROTTA: Statistiche pagamenti MYZ
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

// ROTTA: Sincronizza pagamenti MYZ
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

// ROTTA: Dashboard
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
            wallet_addresses: {
                myz: MYZ_WALLET_ADDRESS,
                xmr: XMR_WALLET_ADDRESS
            }
        }
    });
});

// Avvia server
app.listen(port, '0.0.0.0', () => {
    console.log('🚀 Gateway MyZubster in esecuzione su http://0.0.0.0:' + port);
    console.log('📁 Dati salvati su: ' + DATA_FILE);
    console.log('📊 Pagamenti attuali: ' + payments.length);
    console.log('💰 MYZ Wallet: ' + MYZ_WALLET_ADDRESS);
    console.log('💰 XMR Wallet: ' + XMR_WALLET_ADDRESS);
    console.log('💳 Platform Fee: ' + PLATFORM_FEE + '%');
});
