#!/usr/bin/env python3
"""
Packing Robot - Imballaggio automatico
"""

import time
import random
import json

class PackingRobot:
    def __init__(self):
        self.name = "PackingBot"
        self.status = "idle"
        self.packed_items = []
        self.quality_checks = 0
        self.packing_speed = 1.0
    
    def prepare_package(self, item_id, item_type):
        """Prepara il pacchetto"""
        print(f"📦 Preparazione pacchetto per {item_id} ({item_type})...")
        time.sleep(0.5 * self.packing_speed)
        return True
    
    def pack_item(self, item_id, item_type, quantity=1):
        """Imballa un articolo"""
        print(f"📦 Imballaggio {quantity}x {item_id}...")
        
        # Preparazione
        self.prepare_package(item_id, item_type)
        
        # Imballaggio
        for i in range(quantity):
            print(f"   📦 Articolo {i+1}/{quantity} imballato")
            time.sleep(0.3 * self.packing_speed)
        
        # Controllo qualità
        self.quality_check(item_id)
        
        # Registra
        self.packed_items.append({
            'item_id': item_id,
            'item_type': item_type,
            'quantity': quantity,
            'timestamp': time.time()
        })
        
        print(f"✅ Imballaggio completato: {quantity}x {item_id}")
        return True
    
    def quality_check(self, item_id):
        """Esegue controllo qualità"""
        self.quality_checks += 1
        passed = random.random() > 0.1  # 90% di successo
        if passed:
            print(f"   ✅ Controllo qualità superato per {item_id}")
        else:
            print(f"   ⚠️ Controllo qualità fallito per {item_id} - riprova")
        return passed
    
    def process_order(self, order):
        """Processa un ordine"""
        print(f"\n📋 Processando ordine: {order}")
        for item in order['items']:
            self.pack_item(
                item['id'],
                item['type'],
                item.get('quantity', 1)
            )
        return True
    
    def get_stats(self):
        """Statistiche di imballaggio"""
        return {
            'total_packed': len(self.packed_items),
            'quality_checks': self.quality_checks,
            'packing_speed': self.packing_speed
        }
    
    def run(self):
        """Simula imballaggio"""
        print(f"📦 {self.name} avviato!")
        
        # Simula ordini
        orders = [
            {'items': [{'id': 'BOX-001', 'type': 'electronics', 'quantity': 2}]},
            {'items': [{'id': 'BOX-002', 'type': 'clothing', 'quantity': 3}]},
            {'items': [{'id': 'BOX-003', 'type': 'books', 'quantity': 1}]}
        ]
        
        for order in orders:
            self.process_order(order)
            time.sleep(0.5)
        
        print("\n📊 STATISTICHE IMBALLAGGIO:")
        stats = self.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    robot = PackingRobot()
    robot.run()
