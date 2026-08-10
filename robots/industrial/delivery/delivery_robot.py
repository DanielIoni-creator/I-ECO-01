#!/usr/bin/env python3
"""
Delivery Robot - Consegne autonome
"""

import time
import random
import json
from datetime import datetime

class DeliveryRobot:
    def __init__(self):
        self.name = "DeliveryBot"
        self.status = "idle"
        self.package = None
        self.route = []
        self.deliveries = []
        self.battery = 100
    
    def load_package(self, package_id, destination):
        """Carica un pacco per la consegna"""
        self.package = {
            'id': package_id,
            'destination': destination,
            'status': 'loaded'
        }
        print(f"📦 Pacco {package_id} caricato per {destination}")
    
    def calculate_route(self, start, end):
        """Calcola il percorso ottimale"""
        print(f"🗺️ Calcolo percorso da {start} a {end}...")
        self.route = [
            start,
            (random.randint(0, 100), random.randint(0, 100)),
            end
        ]
        return self.route
    
    def navigate(self, destination):
        """Naviga verso la destinazione"""
        print(f"🧭 Navigando verso {destination}...")
        for waypoint in self.route:
            print(f"   📍 Passaggio da {waypoint}")
            time.sleep(1)
        return True
    
    def deliver_package(self):
        """Esegue la consegna"""
        if not self.package:
            print("❌ Nessun pacco da consegnare")
            return False
        
        self.status = "delivering"
        print(f"🚚 Inizio consegna pacco {self.package['id']}...")
        
        # Naviga verso la destinazione
        route = self.calculate_route((0, 0), self.package['destination'])
        self.navigate(self.package['destination'])
        
        # Consegna
        self.package['status'] = 'delivered'
        self.deliveries.append({
            'package_id': self.package['id'],
            'destination': self.package['destination'],
            'delivered_at': datetime.now().isoformat()
        })
        
        print(f"✅ Pacco {self.package['id']} consegnato!")
        self.status = "idle"
        self.package = None
        return True
    
    def add_delivery(self, package_id, destination):
        """Aggiunge una consegna alla coda"""
        return {
            'package_id': package_id,
            'destination': destination,
            'status': 'pending'
        }
    
    def get_delivery_stats(self):
        """Statistiche consegne"""
        return {
            'total_deliveries': len(self.deliveries),
            'pending': len([d for d in self.deliveries if d.get('status') == 'pending']),
            'completed': len([d for d in self.deliveries if d.get('status') == 'delivered'])
        }
    
    def run(self):
        """Simula un ciclo di consegne"""
        print(f"🚚 {self.name} avviato!")
        
        # Simula consegne
        deliveries = [
            ("PKG001", "Roma"),
            ("PKG002", "Milano"),
            ("PKG003", "Napoli")
        ]
        
        for pkg_id, dest in deliveries:
            self.load_package(pkg_id, dest)
            self.deliver_package()
        
        print("\n📊 STATISTICHE CONSEGNE:")
        stats = self.get_delivery_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    robot = DeliveryRobot()
    robot.run()
