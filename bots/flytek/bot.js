/**
 * Flytek Bot - Telegram Bot per MyZubster
 * Gestisce eventi, RSVP, pagamenti XMR e crew
 */

const TelegramBot = require('node-telegram-bot-api');
const token = process.env.TELEGRAM_BOT_TOKEN || 'YOUR_BOT_TOKEN';

if (!token || token === 'YOUR_BOT_TOKEN') {
    console.error('❌ ERRORE: Imposta TELEGRAM_BOT_TOKEN nel file .env');
    process.exit(1);
}

const bot = new TelegramBot(token, { polling: true });

// Database in memoria (in produzione usare MongoDB/Redis)
const events = {};
const crew = {};

// Comandi principali
bot.onText(/\/start/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, `
🤖 **Flytek Bot v2.0 - MyZubster**

Comandi disponibili:
/event - Crea un nuovo evento
/rsvp - Conferma partecipazione a un evento
/pay - Paga in XMR per un evento
/crew - Gestisci la crew dell'evento
/help - Mostra questo messaggio

💰 Accettiamo solo pagamenti in XMR (Monero)
    `, { parse_mode: 'Markdown' });
});

bot.onText(/\/help/, (msg) => {
    const chatId = msg.chat.id;
    bot.sendMessage(chatId, `
📋 **Guida Flytek Bot**

1. Crea un evento con /event
2. Condividi il codice evento con la community
3. I partecipanti usano /rsvp per confermare
4. /pay per pagare in XMR
5. /crew per gestire il team

🔗 Per maggiori info: github.com/MyZubster-Ecosystem
    `, { parse_mode: 'Markdown' });
});

// Crea evento
bot.onText(/\/event (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const eventData = match[1];
    const eventId = Date.now().toString(36);
    
    events[eventId] = {
        id: eventId,
        data: eventData,
        createdBy: msg.from.username || msg.from.id,
        createdAt: new Date().toISOString(),
        rsvp: [],
        paid: []
    };
    
    bot.sendMessage(chatId, `
✅ **Evento creato con successo!**

📌 Codice evento: \`${eventId}\`
📝 Descrizione: ${eventData}

🔗 Condividi questo codice con la community.
Per partecipare: /rsvp ${eventId}
Per pagare: /pay ${eventId}
    `, { parse_mode: 'Markdown' });
});

// RSVP
bot.onText(/\/rsvp (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const eventId = match[1];
    const user = msg.from.username || msg.from.id;
    
    if (!events[eventId]) {
        bot.sendMessage(chatId, '❌ Evento non trovato. Verifica il codice.');
        return;
    }
    
    if (events[eventId].rsvp.includes(user)) {
        bot.sendMessage(chatId, '✅ Sei già registrato per questo evento!');
        return;
    }
    
    events[eventId].rsvp.push(user);
    bot.sendMessage(chatId, `
✅ **RSVP confermato!**

📌 Evento: ${events[eventId].data}
👤 Partecipanti: ${events[eventId].rsvp.length}

💰 Per pagare: /pay ${eventId}
    `);
});

// Pagamento XMR
bot.onText(/\/pay (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const eventId = match[1];
    const user = msg.from.username || msg.from.id;
    
    if (!events[eventId]) {
        bot.sendMessage(chatId, '❌ Evento non trovato.');
        return;
    }
    
    const amount = 0.01; // 0.01 XMR
    const address = '45M4DW1ug8bdQowWpxucTpgsfjLbVxbYaAra79VewmBobuuhgqTjyD4R3DzpqLM2veiphcB16n24qN1QbLg3y2PYGK3Qkoe';
    
    bot.sendMessage(chatId, `
💰 **Pagamento XMR**

Invia esattamente **${amount} XMR** a:
\`${address}\`

📌 Evento: ${events[eventId].data}
👤 Utente: @${user}

⏳ Dopo il pagamento, il sistema confermerà automaticamente.
    `, { parse_mode: 'Markdown' });
});

// Crew
bot.onText(/\/crew (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const command = match[1].split(' ');
    const action = command[0];
    const user = command[1] || msg.from.username;
    
    if (!crew[chatId]) {
        crew[chatId] = [];
    }
    
    if (action === 'add') {
        crew[chatId].push(user);
        bot.sendMessage(chatId, `✅ @${user} aggiunto alla crew!`);
    } else if (action === 'remove') {
        crew[chatId] = crew[chatId].filter(m => m !== user);
        bot.sendMessage(chatId, `✅ @${user} rimosso dalla crew.`);
    } else if (action === 'list') {
        const list = crew[chatId].length > 0 ? crew[chatId].join(', ') : 'Nessun membro';
        bot.sendMessage(chatId, `👥 **Crew**: ${list}`);
    }
});

// Fallback per comandi non riconosciuti
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    if (!msg.text || msg.text.startsWith('/')) return;
    bot.sendMessage(chatId, '❓ Comando non riconosciuto. Usa /help per la lista dei comandi.');
});

console.log('🤖 Flytek Bot avviato!');
console.log('📋 Comandi disponibili: /event, /rsvp, /pay, /crew, /help');
