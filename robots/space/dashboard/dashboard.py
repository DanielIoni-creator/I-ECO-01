#!/usr/bin/env python3
"""
Space Station Dashboard - Mission Control
"""

import time
import random
from datetime import datetime

class SpaceDashboard:
    def __init__(self):
        self.systems = {
            "energy": 85,
            "oxygen": 92,
            "temperature": 20.5,
            "comms": "active",
            "life_support": "operational"
        }
        self.alerts = []
        self.missions = []
    
    def update_telemetry(self):
        """Aggiorna la telemetria"""
        self.systems["energy"] = random.randint(70, 100)
        self.systems["oxygen"] = random.randint(85, 100)
        self.systems["temperature"] = round(random.uniform(19.0, 22.0), 1)
        print("📊 Telemetry updated")
        return self.systems
    
    def add_alert(self, message, level="info"):
        """Aggiunge un alert"""
        alert = {
            "message": message,
            "level": level,
            "timestamp": datetime.now().isoformat()
        }
        self.alerts.append(alert)
        print(f"🔔 Alert: {message} ({level})")
        return alert
    
    def get_status(self):
        """Stato completo"""
        return {
            "systems": self.systems,
            "alerts": len(self.alerts),
            "missions": len(self.missions),
            "timestamp": datetime.now().isoformat()
        }
    
    def run(self):
        print("🛸 Space Station Dashboard")
        print("="*40)
        
        self.update_telemetry()
        self.add_alert("System check OK", "info")
        
        if self.systems["energy"] < 75:
            self.add_alert("Low energy detected!", "warning")
        
        print("\n📊 STATUS:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    dashboard = SpaceDashboard()
    dashboard.run()
