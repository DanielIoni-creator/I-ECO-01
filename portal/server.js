const express = require('express');
const path = require('path');
const cors = require('cors');
const axios = require('axios');  // Usa axios invece di fetch
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
        const response = await axios.post(`${GATEWAY_URL}/api/pytho/chat`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('❌ Errore proxy chat:', error.message);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Proxy per le statistiche
app.get('/api/myz/stats', async (req, res) => {
    try {
        console.log('📡 Proxy stats');
        const response = await axios.get(`${GATEWAY_URL}/api/myz/stats`);
        res.json(response.data);
    } catch (error) {
        console.error('❌ Errore proxy stats:', error.message);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Proxy per la dashboard
app.get('/api/dashboard', async (req, res) => {
    try {
        console.log('📡 Proxy dashboard');
        const response = await axios.get(`${GATEWAY_URL}/api/dashboard`);
        res.json(response.data);
    } catch (error) {
        console.error('❌ Errore proxy dashboard:', error.message);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Proxy per il time travel
app.post('/api/pytho/timetravel', async (req, res) => {
    try {
        console.log('📡 Proxy time travel:', req.body);
        const response = await axios.post(`${GATEWAY_URL}/api/pytho/timetravel`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('❌ Errore proxy time travel:', error.message);
        res.status(500).json({ success: false, error: error.message });
    }
});

// Proxy per botanical past
app.post('/api/pytho/botanical-past', async (req, res) => {
    try {
        console.log('📡 Proxy botanical past:', req.body);
        const response = await axios.post(`${GATEWAY_URL}/api/pytho/botanical-past`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('❌ Errore proxy botanical past:', error.message);
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(port, () => {
    console.log(`🖥️ Pytho Portal running on http://localhost:${port}`);
    console.log(`🔗 Gateway URL: ${GATEWAY_URL}`);
});
