#!/usr/bin/env python3
"""
Barman Inventory - Gestione inventario automatica
"""

import time
import json
from datetime import datetime

class InventoryManager:
    def __init__(self):
        self.name = "InventoryManager"
        self.inventory = {}
        self.alerts = []
        self.transactions = []
    
    def load_inventory(self):
        """Carica l'inventario iniziale"""
        self.inventory = {
            'Rum': {'quantity': 5000, 'unit': 'ml', 'threshold': 1000},
            'Gin': {'quantity': 3000, 'unit': 'ml', 'threshold': 800},
            'Vodka': {'quantity': 4000, 'unit': 'ml', 'threshold': 900},
            'Campari': {'quantity': 2000, 'unit': 'ml', 'threshold': 500},
            'Aperol': {'quantity': 2500, 'unit': 'ml', 'threshold': 600},
            'Prosecco': {'quantity': 3000, 'unit': 'ml', 'threshold': 700},
            'Menta': {'quantity': 500, 'unit': 'g', 'threshold': 100},
            'Lime': {'quantity': 200, 'unit': 'pz', 'threshold': 50},
            'Zucchero': {'quantity': 1000, 'unit': 'g', 'threshold': 200}
        }
        print(f"📦 Inventario caricato: {len(self.inventory)} prodotti")
        return self.inventory
    
    def update_inventory(self, item, quantity_used):
        """Aggiorna l'inventario dopo l'uso"""
        if item not in self.inventory:
            print(f"❌ Prodotto {item} non trovato")
            return False
        
        self.inventory[item]['quantity'] -= quantity_used
        
        # Registra transazione
        self.transactions.append({
            'item': item,
            'quantity_used': quantity_used,
            'remaining': self.inventory[item]['quantity'],
            'timestamp': datetime.now().isoformat()
        })
        
        # Controlla soglia
        if self.inventory[item]['quantity'] <= self.inventory[item]['threshold']:
            alert = {
                'item': item,
                'message': f"⚠️ Scorte basse per {item}: {self.inventory[item]['quantity']} {self.inventory[item]['unit']}",
                'timestamp': datetime.now().isoformat()
            }
            self.alerts.append(alert)
            print(f"⚠️ {alert['message']}")
        
        print(f"📦 {item}: {self.inventory[item]['quantity']} {self.inventory[item]['unit']} rimanenti")
        return True
    
    def add_stock(self, item, quantity):
        """Aggiunge stock a un prodotto"""
        if item not in self.inventory:
            print(f"❌ Prodotto {item} non trovato")
            return False
        
        self.inventory[item]['quantity'] += quantity
        print(f"📦 {item}: +{quantity} {self.inventory[item]['unit']} aggiunti")
        return True
    
    def get_low_stock_alerts(self):
        """Restituisce gli alert per scorte basse"""
        alerts = []
        for item, data in self.inventory.items():
            if data['quantity'] <= data['threshold']:
                alerts.append({
                    'item': item,
                    'current': data['quantity'],
                    'threshold': data['threshold'],
                    'unit': data['unit']
                })
        return alerts
    
    def get_inventory_report(self):
        """Genera un report dell'inventario"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_items': len(self.inventory),
            'low_stock': len(self.get_low_stock_alerts()),
            'transactions_today': len(self.transactions),
            'inventory': self.inventory
        }
        return report
    
    def run(self):
        """Simula la gestione dell'inventario"""
        print(f"📋 {self.name} avviato!")
        self.load_inventory()
        
        # Simula consumi
        consumi = [
            ('Rum', 200),
            ('Gin', 150),
            ('Vodka', 180),
            ('Lime', 15),
            ('Menta', 30),
            ('Aperol', 120)
        ]
        
        print("\n🔄 Simulazione consumi...")
        for item, quantity in consumi:
            self.update_inventory(item, quantity)
            time.sleep(0.3)
        
        print(f"\n📊 REPORT INVENTARIO:")
        report = self.get_inventory_report()
        print(f"   Totale prodotti: {report['total_items']}")
        print(f"   Scorte basse: {report['low_stock']}")
        print(f"   Transazioni: {report['transactions_today']}")
        
        if report['low_stock'] > 0:
            print("\n⚠️ PRODOTTI CON SCORTE BASSE:")
            for alert in self.get_low_stock_alerts():
                print(f"   - {alert['item']}: {alert['current']} {alert['unit']} (soglia: {alert['threshold']})")

if __name__ == "__main__":
    manager = InventoryManager()
    manager.run()
