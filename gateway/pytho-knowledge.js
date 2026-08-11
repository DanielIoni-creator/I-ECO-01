// ============================================
// PYTHO KNOWLEDGE BASE - Basata sulle issue
// ============================================

const pythoKnowledge = {
    'daniel': [
        '👨‍🌾 Daniel ha creato Pytho per aiutare le persone a coltivare orti sostenibili!',
        '📚 Daniel ha documentato tutto il processo in oltre 100 issue su GitHub.',
        '🌟 Pytho è nato da un\'idea di Daniel per unire blockchain e orti botanici.'
    ],
    'issue': [
        '📋 Pytho si basa sulle issue di GitHub create da Daniel per imparare e crescere.',
        '🔍 Ogni issue è una lezione! Pytho ha imparato da oltre 100 problemi risolti.',
        '📝 Le issue raccontano la storia di MyZubster, dai primi passi al futuro.'
    ],
    'storia': [
        '📜 La storia di MyZubster inizia con Daniel che voleva creare un orto botanico su blockchain.',
        '🌿 Pytho è il guardiano della storia botanica, registrando piante dal 1500 al 3000.',
        '🛸 Il viaggio di Pytho nel tempo è iniziato con la issue #1: "Creare un orto botanico decentralizzato".'
    ],
    'futuro': [
        '🚀 Il futuro di Pytho è guidato dalle issue della community! Ogni contributo conta.',
        '🌌 Pytho diventerà una guida universale per orti botanici, basata sulla conoscenza collettiva.',
        '💚 Daniel e Pytho stanno costruendo un futuro dove ogni orto è tracciato su blockchain.'
    ],
    'piante_issue': [
        '🌱 Le piante recuperate da Pytho sono state documentate nelle issue: Rosa Antica (#42), Lilio (#43), Orchidea Selvatica (#44).',
        '📊 Ogni specie recuperata ha una issue dedicata con dettagli sulla sua storia e coltivazione.',
        '🌿 Le 24 specie di Pytho sono state tutte documentate attraverso le issue di GitHub.'
    ],
    'default': [
        '👽 Pytho sta imparando dalle issue di Daniel! Chiedimi qualcosa su: Daniel, issue, storia, futuro, piante.',
        '📚 Pytho ha imparato da 100+ issue su GitHub. Cosa vuoi sapere sul progetto?'
    ]
};

const pythoKeywords = {
    'daniel': ['daniel', 'creatore', 'fondatore', 'ideatore', 'daniele'],
    'issue': ['issue', 'problemi', 'bug', 'richiesta', 'feature', 'miglioramento'],
    'storia': ['storia', 'passato', 'origine', 'inizio', 'primi passi'],
    'futuro': ['futuro', 'prossimo', 'piano', 'visione', 'obiettivo'],
    'piante_issue': ['pianta', 'specie', 'orto', 'botanico', 'recuperata', 'coltivazione']
};

function getPythoKnowledge(message) {
    const lower = message.toLowerCase();
    let response = 'default';
    
    for (const [category, words] of Object.entries(pythoKeywords)) {
        if (words.some(word => lower.includes(word))) {
            response = category;
            break;
        }
    }
    
    const responses = pythoKnowledge[response] || pythoKnowledge['default'];
    return responses[Math.floor(Math.random() * responses.length)];
}

module.exports = { getPythoKnowledge };
