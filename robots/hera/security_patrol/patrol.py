#!/usr/bin/env python3
"""
HERA Security Patrol — Robot di sicurezza autonomo
"""

import time
import random
import json
from datetime import datetime

class HeraSecurityPatrol:
    def __init__(self):
        self.name = "Hera Security Patrol"
        self.status = "idle"
        self.battery = 100
        self.patrol_route = []
        self.alerts = []
        self.detections = []
        self.area_covered = 0

    def start_patrol(self):
        """Avvia il pattugliamento"""
        self.status = "patrolling"
        print(f"🚨 {self.name} avvia pattugliamento!")
        return True

    def scan_area(self, area_name):
        """Scansiona un'area"""
        print(f"🔍 Scansione area: {area_name}")
        time.sleep(1)
        
        # Simula rilevazioni
        detection = None
        if random.random() < 0.15:  # 15% di probabilità di rilevare qualcosa
            detection = {
                "type": random.choice(["movimento", "rumore", "intrusione", "pacco sospetto"]),
                "area": area_name,
                "timestamp": datetime.now().isoformat()
            }
            self.detections.append(detection)
            self.alerts.append({
                "level": "HIGH" if detection["type"] in ["intrusione", "pacco sospetto"] else "MEDIUM",
                "message": f"⚠️ Rilevato: {detection['type']} in {area_name}",
                "timestamp": datetime.now().isoformat()
            })
            print(f"⚠️ {detection['type']} rilevato!")
        else:
            print("✅ Area sicura")
        
        self.area_covered += 1
        self.battery -= random.randint(2, 5)
        return detection

    def send_alert(self, alert):
        """Invia un alert"""
        print(f"📡 ALERT: {alert['message']}")
        time.sleep(0.5)
        return True

    def get_status(self):
        """Restituisce lo stato del robot"""
        return {
            "name": self.name,
            "status": self.status,
            "battery": self.battery,
            "area_covered": self.area_covered,
            "detections": len(self.detections),
            "alerts": len(self.alerts)
        }

    def run_patrol(self):
        """Esegue un pattugliamento completo"""
        areas = ["ingresso", "corridoio", "parcheggio", "giardino", "magazzino"]
        
        self.start_patrol()
        
        for area in areas:
            print(f"\n📍 Pattugliamento: {area}")
            detection = self.scan_area(area)
            
            if detection and detection["type"] in ["intrusione", "pacco sospetto"]:
                for alert in self.alerts:
                    self.send_alert(alert)
            
            time.sleep(0.5)
        
        self.status = "completed"
        print("\n✅ Pattugliamento completato!")
        print(f"   Aree coperte: {self.area_covered}")
        print(f"   Rilevazioni: {len(self.detections)}")
        print(f"   Allerte: {len(self.alerts)}")

if __name__ == "__main__":
    patrol = HeraSecurityPatrol()
    patrol.run_patrol()
