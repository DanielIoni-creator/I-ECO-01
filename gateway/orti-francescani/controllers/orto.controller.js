/**
 * 🙏 Orti Francescani Controller
 */

const fs = require('fs');
const path = require('path');
const { OrtoFrancescano } = require('../models/orto.model');

const ORTI_FILE = path.join(__dirname, '../orti-francescani.json');

class OrtiFrancescaniController {
    constructor() {
        this.orti = [];
        this.loadOrti();
    }

    loadOrti() {
        try {
            if (fs.existsSync(ORTI_FILE)) {
                const data = fs.readFileSync(ORTI_FILE, 'utf8');
                const ortiData = JSON.parse(data);
                this.orti = ortiData.map(o => new OrtoFrancescano(o));
            }
        } catch (error) {
            console.error('❌ Errore caricamento orti:', error);
            this.orti = [];
        }
    }

    saveOrti() {
        try {
            fs.writeFileSync(ORTI_FILE, JSON.stringify(this.orti.map(o => o.toJSON()), null, 2));
            console.log('✅ Orti salvati:', this.orti.length);
        } catch (error) {
            console.error('❌ Errore salvataggio orti:', error);
        }
    }

    // Registra un nuovo orto
    async registerOrto(req, res) {
        try {
            const data = req.body;
            const orto = new OrtoFrancescano(data);
            this.orti.push(orto);
            this.saveOrti();

            res.status(201).json({
                success: true,
                message: `🙏 Orto "${orto.nome}" registrato con successo!`,
                data: orto.toJSON()
            });
        } catch (error) {
            console.error('❌ Errore registrazione orto:', error);
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Ottieni tutti gli orti
    async getOrti(req, res) {
        try {
            const { stato, citta } = req.query;
            let filtered = this.orti;

            if (stato) {
                filtered = filtered.filter(o => o.stato === stato);
            }
            if (citta) {
                filtered = filtered.filter(o => o.citta === citta);
            }

            res.json({
                success: true,
                data: filtered.map(o => o.toJSON()),
                total: filtered.length
            });
        } catch (error) {
            console.error('❌ Errore recupero orti:', error);
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Ottieni un orto specifico
    async getOrto(req, res) {
        try {
            const { id } = req.params;
            const orto = this.orti.find(o => o.id === id);
            
            if (!orto) {
                return res.status(404).json({
                    success: false,
                    error: 'Orto non trovato'
                });
            }

            res.json({
                success: true,
                data: orto.toJSON()
            });
        } catch (error) {
            console.error('❌ Errore recupero orto:', error);
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Registra una pianta
    async addPlant(req, res) {
        try {
            const { id } = req.params;
            const plantData = req.body;
            
            const orto = this.orti.find(o => o.id === id);
            if (!orto) {
                return res.status(404).json({
                    success: false,
                    error: 'Orto non trovato'
                });
            }

            const plant = orto.addPlant(plantData);
            this.saveOrti();

            // Calcola ricompensa (50 MYZ per pianta)
            const reward = 50;
            const myzAmount = reward;

            res.json({
                success: true,
                message: `🌱 Pianta "${plantData.nome}" registrata! +${myzAmount} MYZ`,
                data: {
                    plant: plant,
                    reward: myzAmount,
                    totale_piante: orto.stats.totale_piante
                }
            });
        } catch (error) {
            console.error('❌ Errore registrazione pianta:', error);
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Statistiche orti
    async getStats(req, res) {
        try {
            const totali = this.orti.length;
            const attivi = this.orti.filter(o => o.stato === 'attivo').length;
            const totale_piante = this.orti.reduce((sum, o) => sum + o.stats.totale_piante, 0);
            const totale_volontari = this.orti.reduce((sum, o) => sum + o.stats.totale_volontari, 0);
            const totale_donazioni = this.orti.reduce((sum, o) => sum + o.stats.totale_donazioni, 0);

            res.json({
                success: true,
                stats: {
                    totali,
                    attivi,
                    totale_piante,
                    totale_volontari,
                    totale_donazioni,
                    media_piante_per_orto: totali > 0 ? (totale_piante / totali).toFixed(1) : 0
                }
            });
        } catch (error) {
            console.error('❌ Errore statistiche:', error);
            res.status(500).json({ success: false, error: error.message });
        }
    }
}

module.exports = { OrtiFrancescaniController };
