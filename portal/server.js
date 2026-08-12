const express = require('express');
const path = require('path');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3002;

app.use(cors());
app.use(express.json());
app.use(express.static(__dirname));

// Rotte statiche
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/css/style.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'css', 'style.css'));
});

app.get('/js/app.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'js', 'app.js'));
});

// Proxy per le API del gateway
const GATEWAY_URL = 'http://localhost:3001';

// Proxy per la chat
app.post('/api/pytho/chat', async (req, res) => {
    try {
        console.log('📡 Proxy chat:', req.body);
        const response = await fetch(`${GATEWAY_URL}/api/pytho/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req.body)
        });
        const data = await response.json();
        console.log('✅ Risposta chat:', data);
        res.json(data);
    } catch (error) {
        console.error('❌ Errore proxy chat:', error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Errore connessione al gateway: ' + error.message 
        });
    }
});

// Proxy per le statistiche MYZ
app.get('/api/myz/stats', async (req, res) => {
    try {
        console.log('📡 Proxy stats');
        const response = await fetch(`${GATEWAY_URL}/api/myz/stats`);
        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error('❌ Errore proxy stats:', error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Errore connessione al gateway: ' + error.message 
        });
    }
});

// Proxy per la dashboard
app.get('/api/dashboard', async (req, res) => {
    try {
        console.log('📡 Proxy dashboard');
        const response = await fetch(`${GATEWAY_URL}/api/dashboard`);
        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error('❌ Errore proxy dashboard:', error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Errore connessione al gateway: ' + error.message 
        });
    }
});

// Proxy per creare pagamenti
app.post('/api/myz/payment/create', async (req, res) => {
    try {
        console.log('📡 Proxy payment:', req.body);
        const response = await fetch(`${GATEWAY_URL}/api/myz/payment/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req.body)
        });
        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error('❌ Errore proxy payment:', error.message);
        res.status(500).json({ 
            success: false, 
            error: 'Errore connessione al gateway: ' + error.message 
        });
    }
});

app.listen(port, () => {
    console.log(`🖥️ Pytho Portal running on http://localhost:${port}`);
    console.log(`🔗 Gateway URL: ${GATEWAY_URL}`);
});

module.exports = app;
