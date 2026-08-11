#!/usr/bin/env python3
"""
XMR Gateway for Space Transactions
"""

import time
import random
from datetime import datetime

class SpaceGateway:
    def __init__(self):
        self.transactions = []
        self.address = "45M4DW1ug8bdQowWpxucTpgsfjLbVxbYaAra79VewmBobuuhgqTjyD4R3DzpqLM2veiphcB16n24qN1QbLg3y2PYGK3Qkoe"
        self.status = "ready"
    
    def create_transaction(self, amount, tag=None):
        """Crea una transazione XMR"""
        tx = {
            "id": f"space_tx_{int(time.time())}",
            "amount": amount,
            "address": self.address,
            "tag": tag,
            "status": "pending",
            "created": datetime.now().isoformat()
        }
        self.transactions.append(tx)
        print(f"💰 Transaction created: {tx['id']}")
        print(f"   Amount: {amount} XMR")
        print(f"   Address: {self.address[:20]}...")
        return tx
    
    def confirm_transaction(self, tx_id):
        """Conferma una transazione"""
        for tx in self.transactions:
            if tx["id"] == tx_id:
                tx["status"] = "confirmed"
                tx["confirmed_at"] = datetime.now().isoformat()
                print(f"✅ Transaction {tx_id} confirmed!")
                return True
        print(f"❌ Transaction {tx_id} not found")
        return False
    
    def get_transactions(self):
        """Lista transazioni"""
        return self.transactions
    
    def run(self):
        print("🚀 XMR Gateway for Space")
        print("="*40)
        
        tx = self.create_transaction(0.01, "SAT-001")
        self.confirm_transaction(tx["id"])
        
        print(f"\n📊 Transazioni: {len(self.transactions)}")

if __name__ == "__main__":
    gateway = SpaceGateway()
    gateway.run()
