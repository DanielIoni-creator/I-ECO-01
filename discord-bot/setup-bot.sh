#!/bin/bash

echo "========================================="
echo "🤖 SETUP BOT DISCORD"
echo "========================================="

# Chiedi il token
echo ""
echo "📝 Inserisci il token del bot (da Discord Developer Portal):"
echo "   (Vai su https://discord.com/developers/applications)"
echo "   Crea una nuova applicazione 'Pytho Bot'"
echo "   Vai su 'Bot' → 'Add Bot' → Copia il TOKEN"
echo ""
read -p "👉 Token: " DISCORD_TOKEN

if [ -z "$DISCORD_TOKEN" ]; then
    echo "❌ Token non inserito!"
    exit 1
fi

# Crea il file .env
cat > .env << EOF
DISCORD_TOKEN=$DISCORD_TOKEN
GATEWAY_URL=http://localhost:3001
