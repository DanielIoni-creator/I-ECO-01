#!/usr/bin/env python3
"""
Sorting Robot - Smistamento automatico
"""

import time
import random
import json

class SortingRobot:
    def __init__(self):
        self.name = "SortingBot"
        self.status = "idle"
        self.items_processed = 0
        self.sorted_items = {}
        self.categories = ["A", "B", "C", "D"]
    
    def scan_item(self, item_id):
        """Scansiona un articolo"""
        print(f"📷 Scansione articolo {item_id}...")
        time.sleep(0.5)
        
        # Simula riconoscimento
        category = random.choice(self.categories)
        print(f"   Categoria rilevata: {category}")
        return category
    
    def sort_item(self, item_id, destination):
        """Smista un articolo nella destinazione"""
        print(f"📦 Smistamento articolo {item_id} verso {destination}...")
        time.sleep(0.5)
        self.items_processed += 1
        print(f"✅ Articolo {item_id} smistato")
        return True
    
    def process_batch(self, items):
        """Processa un batch di articoli"""
        print(f"🔄 Elaborazione batch di {len(items)} articoli...")
        
        for item in items:
            category = self.scan_item(item)
            if category not in self.sorted_items:
                self.sorted_items[category] = []
            self.sorted_items[category].append(item)
            self.sort_item(item, category)
        
        print(f"✅ Batch completato: {len(items)} articoli processati")
    
    def get_stats(self):
        """Statistiche di smistamento"""
        return {
            'total_items': self.items_processed,
            'categories': len(self.sorted_items),
            'distribution': {k: len(v) for k, v in self.sorted_items.items()}
        }
    
    def run(self):
        """Simula smistamento"""
        print(f"📦 {self.name} avviato!")
        
        # Simula batch di articoli
        batches = [
            ["ITEM-001", "ITEM-002", "ITEM-003"],
            ["ITEM-004", "ITEM-005"],
            ["ITEM-006", "ITEM-007", "ITEM-008", "ITEM-009"]
        ]
        
        for batch in batches:
            self.process_batch(batch)
            time.sleep(1)
        
        print("\n📊 STATISTICHE SMISTAMENTO:")
        stats = self.get_stats()
        print(f"   Totale articoli: {stats['total_items']}")
        print(f"   Categorie: {stats['categories']}")
        print("   Distribuzione:")
        for cat, count in stats['distribution'].items():
            print(f"      {cat}: {count} articoli")

if __name__ == "__main__":
    robot = SortingRobot()
    robot.run()
