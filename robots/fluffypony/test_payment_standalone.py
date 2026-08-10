#!/usr/bin/env python3
"""
Test pagamento XMR - Versione standalone
"""

import json
import time
import random

class MockSuperPayGateway:
    def create_order(self, product_id, amount_xmr, description="Drink"):
        order_id = f"order_{random.randint(1000, 9999)}"
        return {
            'order_id': order_id,
            'qr_code': f'monero:45...?amount={amount_xmr}',
            'payment_address': '45M4DW1ug8bdQowWpxucTpgsfjLbVxbYaAra79VewmBobuuhgqTjyD4R3DzpqLM2veiphcB16n24qN1QbLg3y2PYGK3Qkoe',
            'amount': amount_xmr
        }

    def wait_for_payment(self, order_id, timeout=60):
        print("⏳ Simulazione pagamento in corso...")
        time.sleep(3)
        return True

print("🧪 TEST PAGAMENTO XMR")
print("1. Creazione ordine...")
gateway = MockSuperPayGateway()
order = gateway.create_order("drink_001", 0.01, "Test Drink")
print(f"   Ordine: {order['order_id']}")
print(f"   Indirizzo: {order['payment_address']}")
print(f"   QR: {order['qr_code']}")

print("\n2. Attesa pagamento...")
if gateway.wait_for_payment(order['order_id']):
    print("✅ PAGAMENTO RICEVUTO!")
else:
    print("❌ Pagamento fallito")
