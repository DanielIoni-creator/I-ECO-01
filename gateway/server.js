const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

// File di persistenza
const DATA_FILE = path.join(__dirname, 'payments.json');

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

// ROTTA: Crea nuovo pagamento
app.post('/api/cardputer/payment/create', (req, res) => {
    const { tag_id, amount } = req.body;
    
    if (!tag_id || !amount) {
        return res.status(400).json({
            success: false,
            error: 'tag_id e amount sono obbligatori'
        });
    }

    const payment_id = 'pay_' + Date.now() + Math.random().toString(36).substr(2, 5);
    const address = 'xmr_641340aa6aa86029e833a5e5f5fb2b31';
    
    const newPayment = {
        id: payment_id,
        tag_id: tag_id,
        amount: parseFloat(amount),
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
        qr_code: `monero:${address}?amount=${amount}`,
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

// ROTTA: Elimina pagamento (opzionale)
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

// Avvia server
app.listen(port, () => {
    console.log(`Gateway Cardputer in esecuzione su http://localhost:${port}`);
    console.log(`Dati salvati su: ${DATA_FILE}`);
    console.log(`Pagamenti attuali: ${payments.length}`);
});

