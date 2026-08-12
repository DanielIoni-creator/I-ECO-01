#!/bin/bash

echo "========================================="
echo "🧪 TEST MYZUBSTER AI COMPANION"
echo "========================================="

# Test gateway
echo ""
echo "📡 Test Gateway..."
curl -s http://localhost:3001/api/dashboard | jq '.success' 2>/dev/null && echo "✅ Gateway OK" || echo "❌ Gateway offline"

# Test chat
echo ""
echo "🤖 Test Pytho AI..."
curl -s -X POST http://localhost:3001/api/pytho/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Ciao Pytho!"}' | jq '.response' 2>/dev/null || echo "❌ Errore chat"

echo ""
echo "========================================="
echo "✅ Test completato!"
echo "========================================="
