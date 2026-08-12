// ============================================
// RISPOSTE DI PYTHO - VERSIONE COMPLETA
// ============================================

const pythoResponses = {
    'daniel': [
        '👨‍🌾 Daniel Ioni è il creatore di MyZubster e Pytho! Un visionario che unisce blockchain e natura.',
        '🌟 Daniel ha fondato MyZubster per creare un ecosistema sostenibile dove orti botanici e tecnologia si incontrano.',
        '💚 Daniel crede che la tecnologia possa rendere il mondo più verde e decentralizzato.',
        '🚀 Daniel ha ideato Pytho, l\'alieno giardiniere che viaggia nel tempo per salvare le piante!'
    ],
    'chiesa': [
        '⛪ La chiesa è un punto di riferimento spirituale e comunitario per molti paesi.',
        '🌿 In molte comunità, la chiesa gestisce orti e giardini per sostenere i bisognosi.',
        '🌸 Gli orti della chiesa sono spesso luoghi di pace e riflessione, aperti a tutti.',
        '🌻 La chiesa può essere un partner importante per progetti di giardinaggio comunitario.',
        '🙏 Pytho rispetta tutte le fedi e celebra il verde come dono universale.'
    ],
    'myz': [
        '🪙 MYZ è il token nativo dell\'ecosistema MyZubster, basato su blockchain.',
        '🌿 MYZ serve per incentivare la cura degli orti botanici e la sostenibilità.',
        '💰 Con MYZ puoi pagare servizi, acquistare piante e partecipare alla governance.',
        '🌱 Ogni pianta registrata su MyZubster genera ricompense in MYZ.'
    ],
    'monero': [
        '🔶 Monero (XMR) è una criptovaluta focalizzata sulla privacy e l\'anonimato.',
        '🔒 Le transazioni in Monero sono private e non tracciabili.',
        '💰 Monero utilizza firme ad anello e indirizzi stealth per proteggere la privacy.',
        '🌿 MyZubster accetta pagamenti in Monero per transazioni sicure e private.'
    ],
    'fluffypony': [
        '🐴 Fluffypony è il soprannome di Riccardo Spagni, uno dei fondatori di Monero.',
        '🇮🇹 Riccardo Spagni è italiano e ha portato Monero alla ribalta internazionale.',
        '🛡️ Grazie a Fluffypony, Monero ha mantenuto la sua rotta verso la privacy assoluta.',
        '💚 Pytho ammira Fluffypony per la sua dedizione alla privacy e alla libertà.'
    ],
    'musica': [
        '🎵 La musica è l\'anima del mondo vegetale! Le piante reagiscono positivamente alle vibrazioni sonore.',
        '🌿 Gli studi dimostrano che la musica classica favorisce la crescita delle piante.',
        '🎶 Pytho ama la musica! È il sottofondo perfetto per viaggiare nel tempo.',
        '🌻 La musica e la natura sono due facce della stessa medaglia.'
    ],
    'orto': [
        '🌿 Per l\'orto, inizia con piante facili come pomodori, basilico e zucchine.',
        '🌱 Prepara il terreno con compost e concime organico prima di piantare.',
        '🍅 I pomodori amano il sole e l\'acqua regolare. Pianta in primavera!',
        '🥬 Ruota le colture ogni anno per mantenere il terreno fertile.'
    ],
    'piante': [
        '🌺 Basilico, menta, rosmarino e timo sono perfetti per iniziare.',
        '🌸 Le piante aromatiche richiedono poco spazio e sono facili da coltivare.',
        '🌿 Erbe come salvia e origano crescono bene sia in vaso che in terra.'
    ],
    'acqua': [
        '💧 Innaffia al mattino presto, mai quando il sole è alto.',
        '🌿 Le piante hanno bisogno di acqua regolare, ma non esagerare!',
        '💦 Controlla il terreno: se è asciutto, è ora di innaffiare.'
    ],
    'concime': [
        '🌱 Usa concime organico come compost, letame maturo o humus di lombrico.',
        '🧪 Per i pomodori, usa concime ricco di potassio e fosforo.',
        '🌿 Il concime liquido è ottimo per le piante in vaso, ogni 15 giorni.'
    ],
    'malattie': [
        '🔍 Le macchie scure sulle foglie possono essere peronospora o alternariosi.',
        '🐛 Per gli insetti, prova con olio di neem o sapone di Marsiglia.',
        '🌿 Rimuovi le foglie malate per evitare che la malattia si diffonda.'
    ],
    'compost': [
        '♻️ Per il compost: avanzi di frutta, verdura, gusci d\'uovo e foglie secche.',
        '🔄 Gira il compost ogni settimana per aerarlo e accelerare la decomposizione.',
        '🌱 Il compost è pronto quando è scuro, friabile e profuma di terra.'
    ],
    'clima': [
        '🌤️ I pomodori amano il sole e il caldo. Temperature ideali: 20-28°C.',
        '🌡️ Proteggi le piante dal gelo con tessuti non tessuti o pacciame.',
        '🌿 In climi caldi, innaffia più spesso. In climi freddi, riduci l\'acqua.'
    ],
    'potatura': [
        '✂️ Potare i pomodori significa eliminare i polloni (germogli laterali).',
        '🌳 La potatura si fa per favorire la crescita dei frutti e migliorare l\'aria.',
        '🌿 Rimuovi le foglie basali per prevenire malattie fungine.'
    ],
    'semina': [
        '🌱 Semina i pomodori in semenzaio a febbraio-marzo, trapianta a maggio.',
        '🌻 Segui le indicazioni sulla confezione dei semi per profondità e distanza.',
        '🌿 Prima di seminare, prepara il terreno con concime organico.'
    ],
    'help': [
        '👽 Ciao! Sono Pytho. Chiedimi di: Daniel, MYZ, Monero, Fluffypony, chiesa, musica, orto, piante, acqua, concime, malattie, compost, clima, potatura o semina!',
        '🌿 Pytho è un esperto di orti e di MyZubster. Cosa vuoi sapere?',
        '💚 Pytho conosce la storia di MyZubster! Chiedimi di Daniel Ioni e del progetto!'
    ],
    'default': [
        '👽 Non ho capito. Prova a chiedermi di: Daniel, MYZ, Monero, Fluffypony, chiesa, musica, orto, piante, acqua, concime, malattie, compost, clima, potatura o semina!',
        '🌿 Chiedimi qualcosa su MyZubster o sul tuo orto!',
        '💡 Pytho conosce molte cose! Prova a chiedermi qualcosa di specifico.'
    ]
};

function getPythoResponse(message) {
    const lower = message.toLowerCase();
    let response = 'default';
    
    // Parole chiave per ogni categoria
    if (lower.includes('daniel') || lower.includes('ioni') || lower.includes('creatore') || lower.includes('fondatore')) {
        response = 'daniel';
    } else if (lower.includes('chiesa') || lower.includes('parrocchia') || lower.includes('duomo') || lower.includes('religione')) {
        response = 'chiesa';
    } else if (lower.includes('myz') || lower.includes('token') || lower.includes('myzubster')) {
        response = 'myz';
    } else if (lower.includes('monero') || lower.includes('xmr')) {
        response = 'monero';
    } else if (lower.includes('fluffypony') || lower.includes('riccardo') || lower.includes('spagni')) {
        response = 'fluffypony';
    } else if (lower.includes('musica') || lower.includes('canzone') || lower.includes('melodia') || lower.includes('suono')) {
        response = 'musica';
    } else if (lower.includes('help') || lower.includes('aiuto') || lower.includes('consiglio') || lower.includes('suggerimento')) {
        response = 'help';
    } else if (lower.includes('orto') || lower.includes('giardino') || lower.includes('coltivare') || lower.includes('semina')) {
        response = 'orto';
    } else if (lower.includes('pianta') || lower.includes('fiore') || lower.includes('albero') || lower.includes('erba') || lower.includes('aromatica')) {
        response = 'piante';
    } else if (lower.includes('acqua') || lower.includes('innaffiare') || lower.includes('bagnare')) {
        response = 'acqua';
    } else if (lower.includes('concime') || lower.includes('fertilizzante') || lower.includes('nutriente')) {
        response = 'concime';
    } else if (lower.includes('malattia') || lower.includes('funghi') || lower.includes('parassita') || lower.includes('insetto') || lower.includes('macchia')) {
        response = 'malattie';
    } else if (lower.includes('compost') || lower.includes('riciclo')) {
        response = 'compost';
    } else if (lower.includes('clima') || lower.includes('sole') || lower.includes('gelo') || lower.includes('freddo') || lower.includes('caldo')) {
        response = 'clima';
    } else if (lower.includes('potatura') || lower.includes('taglia') || lower.includes('ramo') || lower.includes('polloni')) {
        response = 'potatura';
    } else if (lower.includes('semina') || lower.includes('semi') || lower.includes('germogliare') || lower.includes('trapianto')) {
        response = 'semina';
    }
    
    const responses = pythoResponses[response] || pythoResponses['default'];
    return responses[Math.floor(Math.random() * responses.length)];
}

module.exports = { getPythoResponse };
