/**
 * 📡 NFC Controller - Gestione tag NFC
 */

const crypto = require('crypto');

class NFCController {
    constructor() {
        // Database simulato dei tag NFC
        this.tags = new Map();
        this.keys = new Map();
        this.initSampleTags();
    }

    initSampleTags() {
        // Tag di esempio
        const sampleTags = [
            {
                id: '04:12:34:56:78:9A',
                type: 'Mifare Classic 1K',
                uid: '04:12:34:56:78:9A',
                keys: ['A0B1C2D3E4F5', 'F5E4D3C2B1A0'],
                data: 'Orto San Francesco - Pomodoro',
                registered: true,
                owner: 'Parrocchia San Gaudenzo'
            },
            {
                id: '04:AB:CD:EF:12:34',
                type: 'Mifare Ultralight',
                uid: '04:AB:CD:EF:12:34',
                keys: ['123456789ABC'],
                data: 'Orto San Francesco - Basilico',
                registered: true,
                owner: 'Parrocchia San Gaudenzo'
            }
        ];

        sampleTags.forEach(tag => {
            this.tags.set(tag.id, tag);
            this.keys.set(tag.id, tag.keys);
        });
    }

    // Scansiona tag NFC
    async scanTag(req, res) {
        try {
            const { tagId } = req.body;
            
            if (!tagId) {
                return res.status(400).json({
                    success: false,
                    error: 'tagId richiesto'
                });
            }

            const tag = this.tags.get(tagId);
            
            if (!tag) {
                return res.status(404).json({
                    success: false,
                    error: 'Tag non trovato',
                    tagId: tagId,
                    timestamp: new Date().toISOString()
                });
            }

            // Simula lettura del tag
            const result = {
                success: true,
                tag: {
                    id: tag.id,
                    type: tag.type,
                    uid: tag.uid,
                    data: tag.data,
                    registered: tag.registered,
                    owner: tag.owner
                },
                timestamp: new Date().toISOString()
            };

            res.json(result);
        } catch (error) {
            console.error('❌ Errore scan NFC:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    }

    // Verifica autenticità
    async verifyTag(req, res) {
        try {
            const { tagId } = req.body;
            
            if (!tagId) {
                return res.status(400).json({
                    success: false,
                    error: 'tagId richiesto'
                });
            }

            const tag = this.tags.get(tagId);
            
            if (!tag) {
                return res.status(404).json({
                    success: false,
                    error: 'Tag non trovato',
                    tagId: tagId,
                    timestamp: new Date().toISOString()
                });
            }

            // Simula verifica autenticità
            const isAuthentic = tag.registered && tag.keys && tag.keys.length > 0;

            const result = {
                success: true,
                authentic: isAuthentic,
                tag: {
                    id: tag.id,
                    type: tag.type,
                    registered: tag.registered,
                    keys: tag.keys ? tag.keys.length : 0
                },
                timestamp: new Date().toISOString()
            };

            res.json(result);
        } catch (error) {
            console.error('❌ Errore verifica NFC:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    }

    // Ottieni stato del lettore NFC
    async getStatus(req, res) {
        try {
            const status = {
                success: true,
                reader: {
                    connected: true,
                    model: 'Chameleon Ultra',
                    firmware: 'v2.0.0',
                    supported: ['Mifare Classic', 'Mifare Ultralight', 'Mifare DESFire']
                },
                tags: {
                    total: this.tags.size,
                    registered: Array.from(this.tags.values()).filter(t => t.registered).length
                },
                timestamp: new Date().toISOString()
            };

            res.json(status);
        } catch (error) {
            console.error('❌ Errore status NFC:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    }

    // Registra un nuovo tag
    async registerTag(req, res) {
        try {
            const { tagId, type, data, owner } = req.body;
            
            if (!tagId) {
                return res.status(400).json({
                    success: false,
                    error: 'tagId richiesto'
                });
            }

            // Genera chiavi random
            const keys = [
                crypto.randomBytes(6).toString('hex').toUpperCase(),
                crypto.randomBytes(6).toString('hex').toUpperCase()
            ];

            const newTag = {
                id: tagId,
                type: type || 'Mifare Classic 1K',
                uid: tagId,
                keys: keys,
                data: data || 'Nuovo tag NFC',
                registered: true,
                owner: owner || 'MyZubster',
                createdAt: new Date().toISOString()
            };

            this.tags.set(tagId, newTag);
            this.keys.set(tagId, keys);

            res.status(201).json({
                success: true,
                message: '✅ Tag NFC registrato con successo',
                tag: {
                    id: newTag.id,
                    type: newTag.type,
                    data: newTag.data,
                    owner: newTag.owner,
                    keys: newTag.keys
                },
                timestamp: new Date().toISOString()
            });
        } catch (error) {
            console.error('❌ Errore registrazione NFC:', error);
            res.status(500).json({
                success: false,
                error: error.message
            });
        }
    }
}

module.exports = { NFCController };
