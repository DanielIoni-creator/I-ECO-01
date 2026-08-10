#!/usr/bin/env python3
"""
Hera Security Robot - Robot di sicurezza
"""

import time
import random
from datetime import datetime

class SecurityRobot:
    def __init__(self):
        self.name = "Hera SecurityBot"
        self.status = "patrolling"
        self.battery = 100
        self.patrol_route = []
        self.detections = []
        self.alerts = []
        self.area_coverage = 0  # m²
    
    def start_patrol(self):
        """Avvia il pattugliamento"""
        self.status = "patrolling"
        print("🚨 Inizio pattugliamento...")
        return True
    
    def scan_area(self, area_size):
        """Scansiona un'area"""
        print(f"🔍 Scansione area di {area_size} m²...")
        time.sleep(1)
        
        # Simula rilevazione
        detection = None
        if random.random() < 0.2:  # 20% di probabilità di rilevare qualcosa
            detection = {
                'type': random.choice(['movimento', 'rumore', 'intrusione']),
                'location': (random.randint(0, 100), random.randint(0, 100)),
                'timestamp': datetime.now().isoformat()
            }
            self.detections.append(detection)
            print(f"⚠️ Rilevato: {detection['type']} in {detection['location']}")
            
            # Genera alert
            self.alerts.append({
                'type': detection['type'],
                'level': 'HIGH',
                'message': f"Allerta: {detection['type']} rilevato",
                'timestamp': datetime.now().isoformat()
            })
        else:
            print("✅ Nessuna anomalia rilevata")
        
        self.area_coverage += area_size
        self.battery -= random.randint(2, 5)
        return detection
    
    def send_alert(self, alert):
        """Invia un alert al sistema di sicurezza"""
        print(f"📡 INVIO ALLERTA: {alert['message']}")
        time.sleep(0.5)
        print("✅ Allerta inviata")
        return True
    
    def respond_to_intrusion(self):
        """Risponde a un'intrusione"""
        print("🚨 RISPOSTA A INTRUSIONE!")
        print("🔦 Attivazione torcia e sirena...")
        time.sleep(1)
        print("📹 Attivazione registrazione...")
        time.sleep(0.5)
        print("✅ Risposta completata")
        return True
    
    def get_patrol_stats(self):
        """Statistiche del pattugliamento"""
        return {
            'area_coverage': self.area_coverage,
            'detections': len(self.detections),
            'alerts': len(self.alerts),
            'battery': self.battery,
            'status': self.status
        }
    
    def run(self):
        """Simula pattugliamento di sicurezza"""
        print(f"🚨 {self.name} avviato!")
        
        # Simula pattugliamento in diverse aree
        areas = [
            {'name': 'Ingresso', 'size': 100},
            {'name': 'Corridoio', 'size': 150},
            {'name': 'Parcheggio', 'size': 200}
        ]
        
        self.start_patrol()
        
        for area in areas:
            print(f"\n📍 Pattugliamento: {area['name']}")
            detection = self.scan_area(area['size'])
            
            if detection and detection['type'] in ['intrusione', 'movimento']:
                self.respond_to_intrusion()
                for alert in self.alerts:
                    self.send_alert(alert)
            time.sleep(0.5)
        
        print("\n📊 STATISTICHE PATRUGLIAMENTO:")
        stats = self.get_patrol_stats()
        print(f"   Area coperta: {stats['area_coverage']} m²")
        print(f"   Rilevazioni: {stats['detections']}")
        print(f"   Allerte: {stats['alerts']}")
        print(f"   Batteria: {stats['battery']}%")

if __name__ == "__main__":
    robot = SecurityRobot()
    try:
        robot.run()
    except KeyboardInterrupt:
        print("\n🛑 Robot fermato")
