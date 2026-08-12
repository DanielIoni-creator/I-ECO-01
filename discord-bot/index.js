/**
 * 🤖 Pytho Discord Bot
 * Il bot ufficiale di MyZubster su Discord
 */

const Discord = require('discord.js');
const axios = require('axios');

// Configurazione
const TOKEN = process.env.DISCORD_TOKEN || 'YOUR_BOT_TOKEN';
const GATEWAY_URL = process.env.GATEWAY_URL || 'http://localhost:3001';

const client = new Discord.Client({
    intents: [
        Discord.GatewayIntentBits.Guilds,
        Discord.GatewayIntentBits.GuildMessages,
        Discord.GatewayIntentBits.MessageContent,
        Discord.GatewayIntentBits.GuildMembers,
    ]
});

// Evento ready
client.once('ready', () => {
    console.log(`🤖 Pytho Bot è online!`);
    console.log(`👽 Connesso come ${client.user.tag}`);
    console.log(`🌿 Pronto per aiutare la community!`);
});

// Evento messageCreate
client.on('messageCreate', async (message) => {
    // Ignora messaggi del bot
    if (message.author.bot) return;

    // Comandi
    if (message.content.startsWith('!pytho')) {
        const query = message.content.replace('!pytho', '').trim();
        await handlePythoCommand(message, query);
    }

    if (message.content.startsWith('!bounty')) {
        await handleBountyCommand(message);
    }

    if (message.content.startsWith('!stats')) {
        await handleStatsCommand(message);
    }

    if (message.content.startsWith('!plant')) {
        await handlePlantCommand(message);
    }

    if (message.content.startsWith('!help')) {
        await handleHelpCommand(message);
    }
});

// Comando !pytho
async function handlePythoCommand(message, query) {
    if (!query) {
        return message.reply('👽 Cosa vuoi chiedermi? Usa !pytho [domanda]');
    }

    try {
        const response = await axios.post(`${GATEWAY_URL}/api/pytho/chat`, {
            message: query
        });

        const reply = response.data.response || response.data.pytho_says || '👽 Non ho capito...';
        message.reply(`👽 ${reply}`);
    } catch (error) {
        console.error('Errore Pytho:', error);
        message.reply('❌ Pytho è temporaneamente offline. Riprova più tardi!');
    }
}

// Comando !bounty
async function handleBountyCommand(message) {
    try {
        const response = await axios.get(`${GATEWAY_URL}/api/bounties`);
        const bounties = response.data.data || [];

        if (bounties.length === 0) {
            return message.reply('🎯 Nessun bounty disponibile al momento!');
        }

        const embed = new Discord.EmbedBuilder()
            .setTitle('🎯 Bounty Disponibili')
            .setColor('#8b5cf6')
            .setDescription('Ecco i bounty attualmente disponibili:');

        bounties.slice(0, 5).forEach(b => {
            embed.addFields({
                name: `${b.title}`,
                value: `💰 ${b.bountyAmount} ${b.currency}\n📊 ${b.status}\n🏷️ ${b.tags?.join(', ') || 'Nessun tag'}`,
                inline: false
            });
        });

        embed.setFooter({ text: '👽 Pytho dice: "Ogni bounty è un\'avventura!"' });

        message.reply({ embeds: [embed] });
    } catch (error) {
        console.error('Errore bounty:', error);
        message.reply('❌ Impossibile recuperare i bounty. Riprova più tardi!');
    }
}

// Comando !stats
async function handleStatsCommand(message) {
    try {
        const [dashboardRes, statsRes] = await Promise.all([
            axios.get(`${GATEWAY_URL}/api/dashboard`),
            axios.get(`${GATEWAY_URL}/api/myz/stats`)
        ]);

        const dashboard = dashboardRes.data.dashboard || {};
        const stats = statsRes.data.stats || {};

        const embed = new Discord.EmbedBuilder()
            .setTitle('📊 Statistiche MyZubster')
            .setColor('#8b5cf6')
            .addFields(
                { name: '🌿 Piante Registrate', value: `${dashboard.total_plants || 0}`, inline: true },
                { name: '💰 Pagamenti Totali', value: `${stats.total_payments || 0}`, inline: true },
                { name: '💵 Totale Incassato', value: `${stats.total_amount || 0} MYZ`, inline: true },
                { name: '⏳ In Attesa', value: `${stats.pending || 0}`, inline: true },
                { name: '✅ Completati', value: `${stats.paid || 0}`, inline: true },
                { name: '👥 Utenti', value: `${dashboard.total_users || 0}`, inline: true }
            )
            .setFooter({ text: '👽 Pytho dice: "I dati sono potere!"' });

        message.reply({ embeds: [embed] });
    } catch (error) {
        console.error('Errore stats:', error);
        message.reply('❌ Impossibile recuperare le statistiche. Riprova più tardi!');
    }
}

// Comando !plant
async function handlePlantCommand(message) {
    const query = message.content.replace('!plant', '').trim();
    
    if (!query) {
        return message.reply('🌿 Cerca una pianta! Usa !plant [nome]');
    }

    try {
        const response = await axios.get(`${GATEWAY_URL}/api/botanical/search?q=${encodeURIComponent(query)}`);
        const plants = response.data.results || [];

        if (plants.length === 0) {
            return message.reply(`🌿 Nessuna pianta trovata per "${query}"`);
        }

        const plant = plants[0];
        const embed = new Discord.EmbedBuilder()
            .setTitle(`🌿 ${plant.name}`)
            .setColor('#4caf50')
            .addFields(
                { name: '📋 Nome Comune', value: plant.commonName || 'N/A', inline: true },
                { name: '📅 Epoca', value: `${plant.era || 'N/A'}`, inline: true },
                { name: '📍 Luogo', value: plant.location || 'N/A', inline: true },
                { name: '🏷️ Proprietà', value: plant.properties?.join(', ') || 'N/A', inline: false }
            )
            .setFooter({ text: '👽 Pytho dice: "Ogni pianta racconta una storia!"' });

        message.reply({ embeds: [embed] });
    } catch (error) {
        console.error('Errore plant:', error);
        message.reply('❌ Impossibile cercare la pianta. Riprova più tardi!');
    }
}

// Comando !help
async function handleHelpCommand(message) {
    const embed = new Discord.EmbedBuilder()
        .setTitle('🤖 Comandi Pytho Bot')
        .setColor('#8b5cf6')
        .setDescription('Ecco i comandi disponibili:')
        .addFields(
            { name: '!pytho [domanda]', value: '👽 Chatta con Pytho AI', inline: false },
            { name: '!bounty', value: '🎯 Mostra i bounty disponibili', inline: false },
            { name: '!stats', value: '📊 Mostra le statistiche del progetto', inline: false },
            { name: '!plant [nome]', value: '🌿 Cerca informazioni su una pianta', inline: false },
            { name: '!help', value: '📋 Mostra questo messaggio', inline: false }
        )
        .setFooter({ text: '👽 Pytho dice: "Sono qui per aiutarti!"' });

    message.reply({ embeds: [embed] });
}

// Avvia il bot
client.login(TOKEN);
