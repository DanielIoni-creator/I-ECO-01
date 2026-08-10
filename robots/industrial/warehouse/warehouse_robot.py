#!/usr/bin/env python3
"""
Warehouse Robot - Gestione magazzino automatica
"""

import json
import time
import random
from datetime import datetime

class WarehouseRobot:
    def __init__(self):
        self.name = "WarehouseBot"
        self.status = "idle"
        self.inventory = {}
        self.tasks = []
        self.battery = 100
        self.position = (0, 0)
    
    def load_inventory(self):
        """Carica l'inventario"""
        self.inventory = {
            "A1": {"product": "Box A1", "quantity": 50, "location": (10, 20)},
            "B2": {"product": "Box B2", "quantity": 30, "location": (30, 40)},
            "C3": {"product": "Box C3", "quantity": 20, "location": (50, 60)}
        }
        print(f"📦 Inventario caricato: {len(self.inventory)} prodotti")
    
    def navigate_to(self, target_pos):
        """Naviga verso una posizione"""
        print(f"🧭 Navigando da {self.position} a {target_pos}...")
        time.sleep(1)
        self.position = target_pos
        print(f"📍 Posizione raggiunta: {self.position}")
        return True
    
    def pick_item(self, item_id):
        """Preleva un articolo"""
        if item_id not in self.inventory:
            print(f"❌ Articolo {item_id} non trovato")
            return False
        
        item = self.inventory[item_id]
        if item['quantity'] <= 0:
            print(f"❌ Articolo {item_id} esaurito")
            return False
        
        # Naviga alla posizione
        self.navigate_to(item['location'])
        
        # Preleva l'articolo
        item['quantity'] -= 1
        print(f"📦 Prelevato: {item['product']} (rimanenti: {item['quantity']})")
        return True
    
    def add_task(self, task_type, item_id=None):
        """Aggiunge un task alla coda"""
        task = {
            'id': len(self.tasks) + 1,
            'type': task_type,
            'item_id': item_id,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        print(f"📋 Task aggiunto: {task_type} - {item_id}")
        return task
    
    def process_tasks(self):
        """Processa i task in coda"""
        print(f"🔄 Elaborazione {len(self.tasks)} task...")
        for task in self.tasks:
            if task['status'] == 'pending':
                if task['type'] == 'pick':
                    result = self.pick_item(task['item_id'])
                    task['status'] = 'completed' if result else 'failed'
                elif task['type'] == 'inventory':
                    self.load_inventory()
                    task['status'] = 'completed'
                time.sleep(1)
    
    def get_status(self):
        """Restituisce lo stato del robot"""
        return {
            'name': self.name,
            'status': self.status,
            'battery': self.battery,
            'position': self.position,
            'inventory_count': len(self.inventory),
            'tasks_pending': len([t for t in self.tasks if t['status'] == 'pending'])
        }
    
    def run(self):
        """Loop principale"""
        print(f"🤖 {self.name} avviato!")
        self.load_inventory()
        
        # Simula attività di magazzino
        items = list(self.inventory.keys())
        for _ in range(3):
            item = random.choice(items)
            self.add_task('pick', item)
        
        self.process_tasks()
        
        print("\n📊 STATO FINALE:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    robot = WarehouseRobot()
    robot.run()
