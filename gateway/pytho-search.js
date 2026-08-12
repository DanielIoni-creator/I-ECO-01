// ============================================
// PYTHO SEARCH - Ricerche online con AI
// ============================================

const axios = require('axios');

// Configurazione
const WIKIPEDIA_API = 'https://en.wikipedia.org/api/rest_v1/page/summary/';

// Cache per evitare richieste ripetute
const searchCache = new Map();
const CACHE_DURATION = 3600000; // 1 ora

// Funzione per cercare su Wikipedia
async function searchWikipedia(query) {
    try {
        const cacheKey = `wiki_${query}`;
        if (searchCache.has(cacheKey)) {
            const cached = searchCache.get(cacheKey);
            if (Date.now() - cached.timestamp < CACHE_DURATION) {
                return cached.data;
            }
        }

        const response = await axios.get(`${WIKIPEDIA_API}${encodeURIComponent(query)}`);
        
        if (response.data && response.data.extract) {
            const result = {
                source: 'Wikipedia',
                title: response.data.title || query,
                description: response.data.extract.substring(0, 500),
                url: response.data.content_urls?.desktop?.page || ''
            };
            
            searchCache.set(cacheKey, { data: result, timestamp: Date.now() });
            return result;
        }
        return null;
    } catch (error) {
        console.error('Errore ricerca Wikipedia:', error.message);
        return null;
    }
}

// Funzione per rispondere con informazioni di contesto
async function getContextualResponse(message) {
    const lower = message.toLowerCase();
    
    // Parole chiave che attivano la ricerca
    const searchTriggers = [
        'cerca', 'cercami', 'trova', 'trovami', 'ricerca', 'informazioni', 'chi è', 'cos\'è', 
        'che cos\'è', 'significa', 'spiegami', 'dimmi di', 'parlami di', 'news', 'notizie'
    ];
    
    const isSearch = searchTriggers.some(trigger => lower.includes(trigger));
    
    if (isSearch) {
        // Estrai la query dalla frase
        let query = message;
        for (const trigger of searchTriggers) {
            query = query.replace(new RegExp(trigger, 'i'), '').trim();
        }
        
        if (query.length < 2) {
            return "👽 Cosa vuoi che cerchi? Specifica un argomento!";
        }
        
        const result = await searchWikipedia(query);
        
        if (result) {
            return `🔍 Ho trovato queste informazioni su "${query}":\n\n📌 **${result.title}**\n${result.description}\n\n🔗 ${result.url}`;
        } else {
            return `🌿 Non ho trovato informazioni su "${query}". Prova a riformulare la domanda!`;
        }
    }
    
    return null;
}

module.exports = { searchWikipedia, getContextualResponse };
