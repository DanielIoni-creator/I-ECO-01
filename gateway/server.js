const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// ============================================
// 📋 DATABASE PIANTE
// ============================================
const PLANTS_DB = path.join(__dirname, 'plants.json');

if (!fs.existsSync(PLANTS_DB)) {
    fs.writeFileSync(PLANTS_DB, JSON.stringify([]));
}

// ============================================
// 🪨 DATABASE MINERALI
// ============================================
const MINERALS_DB = path.join(__dirname, 'minerals/minerals.json');

if (!fs.existsSync(path.join(__dirname, 'minerals'))) {
    fs.mkdirSync(path.join(__dirname, 'minerals'));
}
if (!fs.existsSync(MINERALS_DB)) {
    fs.writeFileSync(MINERALS_DB, JSON.stringify([]));
}

// ============================================
// 📝 SISTEMA REGISTRAZIONE UTENTI
// ============================================
const { UserDatabase } = require('./auth/register');
const userDB = new UserDatabase();

// ============================================
// 🌿 BOTANICAL PAST - Piante
// ============================================
app.post('/api/pytho/botanical-past', async (req, res) => {
    try {
        const { location, year, species, register } = req.body;
        console.log('🌿 Botanical Past:', { location, year, species: species?.length, register });
        
        if (!species || !Array.isArray(species) || species.length === 0) {
            return res.status(400).json({
                success: false,
                error: 'Specificare almeno una specie'
            });
        }
        
        let plants = [];
        if (fs.existsSync(PLANTS_DB)) {
            plants = JSON.parse(fs.readFileSync(PLANTS_DB, 'utf8'));
        }
        
        const newSpecies = species.map(name => ({
            id: `plant_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
            name: name.trim(),
            location: location || 'Sconosciuto',
            year: parseInt(year) || 0,
            registered: register !== false,
            timestamp: new Date().toISOString()
        }));
        
        plants.push(...newSpecies);
        fs.writeFileSync(PLANTS_DB, JSON.stringify(plants, null, 2));
        
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
        res.status(500).json({ success: false, error: error.message });
    }
});

// ============================================
// 🪨 ROTTE MINERALI
// ============================================
function loadMinerals() {
    try {
        if (fs.existsSync(MINERALS_DB)) {
            return JSON.parse(fs.readFileSync(MINERALS_DB, 'utf8'));
        }
        return [];
    } catch (error) {
        console.error('❌ Errore caricamento minerali:', error);
        return [];
    }
}

function saveMinerals(minerals) {
    try {
        fs.writeFileSync(MINERALS_DB, JSON.stringify(minerals, null, 2));
        console.log('✅ Minerali salvati:', minerals.length);
    } catch (error) {
        console.error('❌ Errore salvataggio minerali:', error);
    }
}

app.post('/api/minerals/register', async (req, res) => {
    try {
        const { location, year, minerals: mineralList } = req.body;
        console.log('🪨 Registrazione minerali:', { location, year, count: mineralList?.length });
        
        if (!mineralList || !Array.isArray(mineralList)) {
            return res.status(400).json({ success: false, error: 'Lista minerali richiesta' });
        }

        const existing = loadMinerals();
        const newMinerals = mineralList.map(m => ({
            id: `mineral_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
            name: m.name,
            location: location,
            year: year,
            properties: m.properties || [],
            symbol: m.symbol || 'N/A',
            hardness: m.hardness || 0,
            color: m.color || 'N/A',
            uses: m.uses || [],
            registered: true,
            timestamp: new Date().toISOString()
        }));

        existing.push(...newMinerals);
        saveMinerals(existing);

        res.json({
            success: true,
            message: `✅ ${mineralList.length} minerali registrati da ${location} (${year})`,
            location: location,
            year: year,
            minerals: newMinerals,
            total: existing.length
        });
    } catch (error) {
        console.error('❌ Errore registrazione minerali:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/api/minerals/all', async (req, res) => {
    try {
        const minerals = loadMinerals();
        res.json({ success: true, data: minerals, total: minerals.length });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/api/minerals/era/:era', async (req, res) => {
    try {
        const minerals = loadMinerals();
        const filtered = minerals.filter(m => m.year == req.params.era);
        res.json({ success: true, data: filtered, total: filtered.length });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// ============================================
// 📋 LISTA PIANTE
// ============================================
app.get('/api/pytho/all-species', async (req, res) => {
    try {
        if (!fs.existsSync(PLANTS_DB)) {
            return res.json([]);
        }
        const plants = JSON.parse(fs.readFileSync(PLANTS_DB, 'utf8'));
        res.json(plants);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/pytho/species-by-era', async (req, res) => {
    try {
        const { era } = req.query;
        if (!era) {
            return res.status(400).json({ error: 'Specificare era (es: era=1500)' });
        }
        if (!fs.existsSync(PLANTS_DB)) {
            return res.json([]);
        }
        const plants = JSON.parse(fs.readFileSync(PLANTS_DB, 'utf8'));
        const filtered = plants.filter(p => p.year == era);
        res.json(filtered);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/pytho/species-count', async (req, res) => {
    try {
        if (!fs.existsSync(PLANTS_DB)) {
            return res.json({ total: 0 });
        }
        const plants = JSON.parse(fs.readFileSync(PLANTS_DB, 'utf8'));
        res.json({ total: plants.length });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================
// 🛸 TIME TRAVEL
// ============================================
app.post('/api/pytho/timetravel', async (req, res) => {
    const { destination, year } = req.body;
    res.json({
        success: true,
        travel: {
            timestamp: new Date().toISOString(),
            destination: destination || 'Sconosciuto',
            year: year || 0,
            status: '🛸 Viaggio completato!',
            pytho: '👽 Il tempo è un concetto umano...',
            flux: '1.21 GW ⚡'
        }
    });
});

// ============================================
// 💰 PAGAMENTI
// ============================================
app.get('/api/myz/stats', async (req, res) => {
    res.json({
        success: true,
        stats: {
            total_payments: 8,
            total_amount: 14900.9,
            total_fee: 303.6,
            pending: 1,
            paid: 7,
            synced: 7
        }
    });
});

// ============================================
// 🙏 ORTI FRANCESCANI
// ============================================
const ortiFrancescaniRoutes = require('./orti-francescani/routes/orto.routes.js');
app.use('/api/orti-francescani', ortiFrancescaniRoutes);

// ============================================
// 📝 ROTTE REGISTRAZIONE
// ============================================
app.post('/api/auth/register', async (req, res) => {
    try {
        const result = await userDB.register(req.body);
        if (result.success) {
            res.status(201).json(result);
        } else {
            res.status(400).json(result);
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/auth/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        const result = await userDB.login(email, password);
        if (result.success) {
            res.json(result);
        } else {
            res.status(401).json(result);
        }
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/api/auth/profile/:id', async (req, res) => {
    try {
        const user = userDB.getUserById(req.params.id);
        if (!user) {
            return res.status(404).json({ success: false, error: 'Utente non trovato' });
        }
        res.json({
            success: true,
            user: {
                id: user.id,
                email: user.email,
                nome: user.nome,
                cognome: user.cognome,
                ruolo: user.ruolo,
                wallet: user.wallet,
                stats: user.stats
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/api/auth/stats', async (req, res) => {
    try {
        const stats = userDB.getStats();
        res.json({ success: true, stats });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.get('/api/auth/wallet/:id', async (req, res) => {
    try {
        const wallet = userDB.getWallet(req.params.id);
        if (!wallet) {
            return res.status(404).json({ success: false, error: 'Wallet non trovato' });
        }
        res.json({ success: true, wallet });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// ============================================
// 📊 DASHBOARD
// ============================================
app.get('/api/dashboard', async (req, res) => {
    try {
        let plants = [];
        if (fs.existsSync(PLANTS_DB)) {
            plants = JSON.parse(fs.readFileSync(PLANTS_DB, 'utf8'));
        }
        
        res.json({
            success: true,
            dashboard: {
                total_plants: plants.length,
                species_by_era: {
                    '-3000': plants.filter(p => p.year == -3000).length,
                    1500: plants.filter(p => p.year == 1500).length,
                    1800: plants.filter(p => p.year == 1800).length,
                    2124: plants.filter(p => p.year == 2124).length
                },
                recent: plants.slice(-5)
            }
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// ============================================
// 🚀 AVVIA IL SERVER
// ============================================
app.listen(port, () => {
    console.log(`🚀 Pytho Temporal su porta ${port}`);
    console.log(`👽 Macchina del tempo attiva!`);
    console.log(`🛸 http://localhost:${port}/temporal`);
    console.log(`📊 http://localhost:${port}/api/dashboard`);
    console.log(`🪨 Minerali: http://localhost:${port}/api/minerals/all`);
    console.log(`🙏 Orti Francescani: http://localhost:${port}/api/orti-francescani`);
});

// ============================================
// 👛 ROTTE WALLET
// ============================================

// Aggiungi MYZ al wallet
app.post('/api/auth/wallet/myz/add', async (req, res) => {
    try {
        const { userId, amount } = req.body;
        if (!userId || !amount) {
            return res.status(400).json({
                success: false,
                error: 'userId e amount sono richiesti'
            });
        }
        const user = userDB.addMYZ(userId, amount);
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'Utente non trovato'
            });
        }
        res.json({
            success: true,
            message: `✅ ${amount} MYZ aggiunti al wallet`,
            wallet: user.wallet
        });
    } catch (error) {
        console.error('❌ Errore aggiunta MYZ:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Aggiungi XMR al wallet
app.post('/api/auth/wallet/xmr/add', async (req, res) => {
    try {
        const { userId, amount } = req.body;
        if (!userId || !amount) {
            return res.status(400).json({
                success: false,
                error: 'userId e amount sono richiesti'
            });
        }
        const user = userDB.addXMR(userId, amount);
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'Utente non trovato'
            });
        }
        res.json({
            success: true,
            message: `✅ ${amount} XMR aggiunti al wallet`,
            wallet: user.wallet
        });
    } catch (error) {
        console.error('❌ Errore aggiunta XMR:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// ============================================
// 👛 ROTTE WALLET XMR E MYZ
// ============================================

// Genera indirizzo wallet
function generateWalletAddress(currency) {
    const crypto = require('crypto');
    const prefix = currency === 'MYZ' ? 'myz' : 'xmr';
    return `${prefix}_${crypto.randomBytes(20).toString('hex')}`;
}

// Ottieni wallet utente
app.get('/api/wallet/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        const user = userDB.getUserById(userId);
        
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'Utente non trovato'
            });
        }
        
        res.json({
            success: true,
            wallet: user.wallet
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Crea un nuovo pagamento MYZ
app.post('/api/payment/myz/create', async (req, res) => {
    try {
        const { userId, amount, description } = req.body;
        const user = userDB.getUserById(userId);
        
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'Utente non trovato'
            });
        }
        
        const payment = {
            id: `pay_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
            userId: userId,
            amount: amount || 0,
            currency: 'MYZ',
            description: description || 'Pagamento MYZ',
            address: user.wallet.myz.address,
            status: 'pending',
            createdAt: new Date().toISOString()
        };
        
        // Salva il pagamento (in un file o database)
        // Per ora lo salviamo in un array
        if (!global.payments) global.payments = [];
        global.payments.push(payment);
        
        res.json({
            success: true,
            payment: payment,
            message: '✅ Pagamento MYZ creato con successo!'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Crea un nuovo pagamento XMR
app.post('/api/payment/xmr/create', async (req, res) => {
    try {
        const { userId, amount, description } = req.body;
        const user = userDB.getUserById(userId);
        
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'Utente non trovato'
            });
        }
        
        const payment = {
            id: `pay_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
            userId: userId,
            amount: amount || 0,
            currency: 'XMR',
            description: description || 'Pagamento XMR',
            address: user.wallet.xmr.address,
            status: 'pending',
            createdAt: new Date().toISOString()
        };
        
        if (!global.payments) global.payments = [];
        global.payments.push(payment);
        
        res.json({
            success: true,
            payment: payment,
            message: '✅ Pagamento XMR creato con successo!'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Aggiorna stato pagamento
app.put('/api/payment/:paymentId/status', async (req, res) => {
    try {
        const { paymentId } = req.params;
        const { status } = req.body;
        
        if (!global.payments) {
            return res.status(404).json({
                success: false,
                error: 'Nessun pagamento trovato'
            });
        }
        
        const payment = global.payments.find(p => p.id === paymentId);
        if (!payment) {
            return res.status(404).json({
                success: false,
                error: 'Pagamento non trovato'
            });
        }
        
        payment.status = status;
        payment.updatedAt = new Date().toISOString();
        
        // Se il pagamento è completato, aggiungi il saldo al wallet dell'utente
        if (status === 'completed') {
            const user = userDB.getUserById(payment.userId);
            if (user) {
                if (payment.currency === 'MYZ') {
                    user.wallet.myz.balance += payment.amount;
                    user.stats.myz_guadagnati += payment.amount;
                } else if (payment.currency === 'XMR') {
                    user.wallet.xmr.balance += payment.amount;
                }
                user.stats.transazioni += 1;
                userDB.saveUsers();
            }
        }
        
        res.json({
            success: true,
            payment: payment,
            message: '✅ Stato pagamento aggiornato con successo!'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Ottieni tutti i pagamenti di un utente
app.get('/api/payments/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        
        if (!global.payments) {
            return res.json({
                success: true,
                payments: [],
                total: 0
            });
        }
        
        const userPayments = global.payments.filter(p => p.userId === userId);
        
        res.json({
            success: true,
            payments: userPayments,
            total: userPayments.length
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});
