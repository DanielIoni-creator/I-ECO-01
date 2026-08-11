// ============================================
// PYTHO AI - Integrazione con Ollama
// ============================================

const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

// Configurazione
const AI_MODEL = process.env.PYTHO_AI_MODEL || 'mistral';
const AI_TIMEOUT = 30000; // 30 secondi

async function getAIResponse(message, context) {
    try {
        // Costruisci il prompt con il contesto di Pytho
        const prompt = `Sei Pytho, l'alieno giardiniere di MyZubster. 
Sei un'esperto di orti botanici, piante, sostenibilità e blockchain.
Rispondi in modo amichevole, con emoji, e in italiano.

Contesto: ${context || 'Sei un assistente per orti e giardini'}

Domanda: ${message}

Risposta:`;

        // Usa Ollama per generare la risposta
        const command = `ollama run ${AI_MODEL} "${prompt}"`;
        const { stdout, stderr } = await execPromise(command, {
            timeout: AI_TIMEOUT
        });

        if (stderr) {
            console.error('Errore AI:', stderr);
            return null;
        }

        return stdout.trim();
    } catch (error) {
        console.error('Errore generazione AI:', error.message);
        return null;
    }
}

// Funzione per rispondere con AI o fallback
async function getPythoAIResponse(message, history = []) {
    // Prima prova con l'AI
    let response = await getAIResponse(message, history.join('\n'));
    
    // Se l'AI non risponde, usa le risposte predefinite
    if (!response) {
        console.log('⚠️ AI non disponibile, uso risposte predefinite');
        const { getPythoResponse } = require('./server.js');
        response = getPythoResponse(message);
    }
    
    return response;
}

module.exports = { getPythoAIResponse };
