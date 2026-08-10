#!/bin/bash
# Script per aggiornare il repository

echo "🔄 Aggiornamento I-ECO-01..."
git pull origin main
git add .
git commit -m "chore: aggiornamento automatico $(date)"
git push origin main
echo "✅ Aggiornato!"
