// ============================================
// PYTHO NEWS - Connessione con le notizie online
// ============================================

const https = require('https');
const http = require('http');

// Configurazione
const NEWS_API_URL = 'https://api.rss2json.com/v1/api.json';
const RSS_FEEDS = [
    'https://www.ansa.it/sito/notizie/economia/economia_rss.xml',
    'https://www.repubblica.it/rss/homepage/rss2.0.xml',
    'https://www.corriere.it/rss/homepage.xml',
    'https://www.ilsole24ore.com/rss/homepage.xml'
];

// Parole chiave per filtrare le notizie rilevanti per Daniel
const danielInterests = [
    'monero', 'xmr', 'cryptocurrency', 'blockchain', 'privacy', 
    'giardino', 'orto', 'piante', 'botanica', 'sostenibilità',
    'comuni', 'città', 'verde urbano', 'ecologia', 'ambiente',
    'open source', 'software', 'tecnologia', 'innovazione',
    'italia', 'roma', 'napoli', 'palermo', 'firenze', 'milano',
    'chiesa', 'musica', 'arte', 'cultura', 'storia'
];

// Cache delle notizie
let newsCache = [];
let lastFetch = null;
const CACHE_DURATION = 1800000; // 30 minuti

// Funzione per fetchare le notizie
function fetchNews() {
    return new Promise((resolve) => {
        const url = `${NEWS_API_URL}?rss_url=${encodeURIComponent(RSS_FEEDS[0])}&api_key=0b8a8a0b8a8a0b8a8a0b8a8a0b8a8a0b&count=20`;
        
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve(json.items || []);
                } catch (e) {
                    resolve([]);
                }
            });
        }).on('error', () => {
            resolve([]);
        });
    });
}

// Funzione per filtrare le notizie rilevanti per Daniel
function filterNewsForDaniel(newsItems) {
    return newsItems.filter(item => {
        const title = (item.title || '').toLowerCase();
        const description = (item.description || '').toLowerCase();
        const content = (item.content || '').toLowerCase();
        const text = title + ' ' + description + ' ' + content;
        
        return danielInterests.some(keyword => text.includes(keyword.toLowerCase()));
    });
}

// Funzione per ottenere le notizie
async function getDanielNews() {
    try {
        const now = Date.now();
        if (newsCache.length > 0 && (now - lastFetch) < CACHE_DURATION) {
            return newsCache;
        }
        
        const allNews = await fetchNews();
        const filteredNews = filterNewsForDaniel(allNews);
        newsCache = filteredNews;
        lastFetch = now;
        return filteredNews;
    } catch (e) {
        return newsCache.length > 0 ? newsCache : [];
    }
}

// Funzione per generare una risposta basata sulle notizie
function generateNewsResponse(newsItems, query) {
    if (newsItems.length === 0) {
        return '📰 Non ho trovato notizie recenti legate ai tuoi interessi, Daniel. Prova più tardi!';
    }
    
    const limited = newsItems.slice(0, 5);
    let response = '📰 **Ecco le notizie che potrebbero interessarti, Daniel:**\n\n';
    
    limited.forEach((item, index) => {
        const title = item.title || 'Titolo non disponibile';
        const link = item.link || '#';
        const date = item.pubDate ? new Date(item.pubDate).toLocaleDateString('it-IT') : 'data sconosciuta';
        response += `${index + 1}. **${title}**\n   📅 ${date}\n   🔗 ${link}\n\n`;
    });
    
    if (newsItems.length > 5) {
        response += `📌 *E altre ${newsItems.length - 5} notizie...*`;
    }
    
    return response;
}

// Funzione per rispondere alle domande con le notizie
async function getPythoNewsResponse(message) {
    const lower = message.toLowerCase();
    const news = await getDanielNews();
    
    if (lower.includes('notizie') || lower.includes('news') || lower.includes('aggiornamenti')) {
        return generateNewsResponse(news, message);
    }
    
    if (lower.includes('cosa succede') || lower.includes('novità') || lower.includes('ultime')) {
        return generateNewsResponse(news, message);
    }
    
    // Cerca notizie specifiche per parola chiave
    for (const interest of danielInterests) {
        if (lower.includes(interest)) {
            const relevant = news.filter(item => {
                const text = (item.title + ' ' + item.description + ' ' + item.content).toLowerCase();
                return text.includes(interest);
            });
            
            if (relevant.length > 0) {
                return generateNewsResponse(relevant, message);
            }
        }
    }
    
    return null;
}

module.exports = { getPythoNewsResponse, danielInterests };
