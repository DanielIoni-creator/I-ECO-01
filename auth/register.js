/**
 * 📝 Sistema di Registrazione Utenti
 * Con database JSON (senza MongoDB)
 */

const fs = require('fs');
const path = require('path');
const bcrypt = require('bcrypt');
const crypto = require('crypto');

const USERS_FILE = path.join(__dirname, '../data/users.json');

class UserDatabase {
    constructor() {
        this.users = [];
        this.loadUsers();
    }

    loadUsers() {
        try {
            if (fs.existsSync(USERS_FILE)) {
                const data = fs.readFileSync(USERS_FILE, 'utf8');
                this.users = JSON.parse(data);
                console.log(`📊 Caricati ${this.users.length} utenti`);
            }
        } catch (error) {
            console.error('❌ Errore caricamento utenti:', error);
            this.users = [];
        }
    }

    saveUsers() {
        try {
            fs.writeFileSync(USERS_FILE, JSON.stringify(this.users, null, 2));
            console.log('✅ Utenti salvati!');
        } catch (error) {
            console.error('❌ Errore salvataggio utenti:', error);
        }
    }

    async register(userData) {
        try {
            const existing = this.users.find(u => u.email === userData.email);
            if (existing) {
                return {
                    success: false,
                    error: 'Email già registrata'
                };
            }

            const salt = await bcrypt.genSalt(10);
            const hashedPassword = await bcrypt.hash(userData.password, salt);

            const newUser = {
                id: `user_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`,
                email: userData.email,
                password: hashedPassword,
                nome: userData.nome || '',
                cognome: userData.cognome || '',
                ruolo: userData.ruolo || 'user',
                telefono: userData.telefono || '',
                indirizzo: userData.indirizzo || '',
                citta: userData.citta || '',
                parrocchia: userData.parrocchia || '',
                orto: userData.orto || null,
                stats: {
                    piante_registrate: 0,
                    myz_guadagnati: 0,
                    orti_creati: 0,
                    volontariato: 0
                },
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
                lastLogin: null,
                attivo: true,
                email_verificato: false
            };

            this.users.push(newUser);
            this.saveUsers();

            return {
                success: true,
                user: {
                    id: newUser.id,
                    email: newUser.email,
                    nome: newUser.nome,
                    cognome: newUser.cognome,
                    ruolo: newUser.ruolo
                },
                message: '✅ Registrazione completata!'
            };
        } catch (error) {
            console.error('❌ Errore registrazione:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    async login(email, password) {
        try {
            const user = this.users.find(u => u.email === email);
            if (!user) {
                return {
                    success: false,
                    error: 'Email o password non validi'
                };
            }

            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) {
                return {
                    success: false,
                    error: 'Email o password non validi'
                };
            }

            user.lastLogin = new Date().toISOString();
            this.saveUsers();

            return {
                success: true,
                user: {
                    id: user.id,
                    email: user.email,
                    nome: user.nome,
                    cognome: user.cognome,
                    ruolo: user.ruolo,
                    stats: user.stats
                },
                message: '✅ Login effettuato!'
            };
        } catch (error) {
            console.error('❌ Errore login:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }

    getUserById(id) {
        return this.users.find(u => u.id === id);
    }

    updateUser(id, data) {
        const user = this.users.find(u => u.id === id);
        if (!user) return null;

        Object.assign(user, data);
        user.updatedAt = new Date().toISOString();
        this.saveUsers();
        return user;
    }

    addPlantToUser(userId) {
        const user = this.users.find(u => u.id === userId);
        if (!user) return null;

        user.stats.piante_registrate += 1;
        user.stats.myz_guadagnati += 50;
        this.saveUsers();
        return user;
    }

    createOrtoForUser(userId, ortoId) {
        const user = this.users.find(u => u.id === userId);
        if (!user) return null;

        user.orto = ortoId;
        user.stats.orti_creati += 1;
        this.saveUsers();
        return user;
    }

    getStats() {
        const total = this.users.length;
        const attivi = this.users.filter(u => u.attivo).length;
        const totalPiante = this.users.reduce((sum, u) => sum + u.stats.piante_registrate, 0);
        const totalMYZ = this.users.reduce((sum, u) => sum + u.stats.myz_guadagnati, 0);
        const totalOrti = this.users.reduce((sum, u) => sum + u.stats.orti_creati, 0);

        return {
            total,
            attivi,
            totalPiante,
            totalMYZ,
            totalOrti
        };
    }
}

module.exports = { UserDatabase };
