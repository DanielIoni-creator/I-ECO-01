
// ============================================
// 📝 ROTTE DI REGISTRAZIONE
// ============================================
const { UserDatabase } = require('./auth/register');
const userDB = new UserDatabase();

// Registrazione utente
app.post('/api/auth/register', async (req, res) => {
    try {
        const result = await userDB.register(req.body);
        if (result.success) {
            res.status(201).json(result);
        } else {
            res.status(400).json(result);
        }
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Login utente
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
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Ottieni profilo utente
app.get('/api/auth/profile/:id', async (req, res) => {
    try {
        const user = userDB.getUserById(req.params.id);
        if (!user) {
            return res.status(404).json({
                success: false,
                error: 'Utente non trovato'
            });
        }
        res.json({
            success: true,
            user: {
                id: user.id,
                email: user.email,
                nome: user.nome,
                cognome: user.cognome,
                ruolo: user.ruolo,
                stats: user.stats,
                createdAt: user.createdAt
            }
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Statistiche utenti
app.get('/api/auth/stats', async (req, res) => {
    try {
        const stats = userDB.getStats();
        res.json({
            success: true,
            stats
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});
