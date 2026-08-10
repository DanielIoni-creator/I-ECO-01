#!/usr/bin/env python3
import json
import time
import requests
from payment_gateway import MockSuperPayGateway

# Usa il mock per testare il flusso
gateway = MockSuperPayGateway()

print("🧪 TEST PAGAMENTO XMR")
print("1. Creazione ordine...")
order = gateway.create_order("drink_001", 0.01, "Test Drink")
print(f"   Ordine: {order['order_id']}")
print(f"   Indirizzo: {order['payment_address']}")
print(f"   QR: {order['qr_code']}")

print("\n2. Attesa pagamento...")
if gateway.wait_for_payment(order['order_id']):
    print("✅ PAGAMENTO RICEVUTO!")
else:
    print("❌ Pagamento fallito")
