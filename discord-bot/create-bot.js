/**
 * 🤖 Creazione Bot Discord via API
 */

const axios = require('axios');

// Configurazione
const TOKEN = process.env.DISCORD_TOKEN || 'IL_TUO_TOKEN_QUI';
const BOT_NAME = 'Pytho Bot';

async function createBot() {
    try {
        console.log('🤖 Creazione bot Discord...');
        
        // Crea l'applicazione
        const appResponse = await axios.post(
            'https://discord.com/api/v10/applications',
            {
                name: BOT_NAME
            },
            {
                headers: {
                    'Authorization': `Bot ${TOKEN}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        
        console.log('✅ Applicazione creata:', appResponse.data.id);
        
        // Crea il bot
        const botResponse = await axios.post(
            `https://discord.com/api/v10/applications/${appResponse.data.id}/bot`,
            {},
            {
                headers: {
                    'Authorization': `Bot ${TOKEN}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        
        console.log('✅ Bot creato:', botResponse.data.token);
        console.log('📝 Token Bot:', botResponse.data.token);
        
        return botResponse.data.token;
    } catch (error) {
        console.error('❌ Errore:', error.response?.data || error.message);
    }
}

createBot();
