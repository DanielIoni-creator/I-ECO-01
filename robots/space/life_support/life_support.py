#!/usr/bin/env python3
"""
Life Support System - Space Station
"""

import time
import random
from datetime import datetime

class LifeSupport:
    def __init__(self):
        self.oxygen = 100
        self.co2 = 0
        self.temperature = 20.5
        self.humidity = 45
        self.water = 100
        self.alerts = []
    
    def monitor_environment(self):
        """Monitora l'ambiente"""
        self.oxygen -= random.uniform(0.1, 0.5)
        self.co2 += random.uniform(0.1, 0.3)
        self.temperature += random.uniform(-0.3, 0.3)
        self.humidity += random.uniform(-1, 1)
        
        print("🌿 Environment monitoring:")
        print(f"   Oxygen: {self.oxygen:.1f}%")
        print(f"   CO2: {self.co2:.1f}%")
        print(f"   Temperature: {self.temperature:.1f}°C")
        print(f"   Humidity: {self.humidity:.1f}%")
        print(f"   Water: {self.water:.1f}%")
        
        self.check_alerts()
        return True
    
    def check_alerts(self):
        """Controlla e genera allarmi"""
        if self.oxygen < 80:
            self.alerts.append(f"⚠️ LOW OXYGEN: {self.oxygen:.1f}%")
            print("🚨 ALERT: Low oxygen detected!")
        if self.co2 > 3:
            self.alerts.append(f"⚠️ HIGH CO2: {self.co2:.1f}%")
            print("🚨 ALERT: High CO2 detected!")
        if self.temperature > 25 or self.temperature < 15:
            self.alerts.append(f"⚠️ TEMP OUT OF RANGE: {self.temperature:.1f}°C")
            print("🚨 ALERT: Temperature out of range!")
    
    def activate_purification(self):
        """Attiva sistema di purificazione"""
        print("🔬 Activating purification system...")
        time.sleep(1)
        self.co2 = max(0, self.co2 - 0.5)
        self.oxygen = min(100, self.oxygen + 0.3)
        print("✅ Purification complete")
        return True
    
    def get_status(self):
        """Stato completo"""
        return {
            "oxygen": round(self.oxygen, 1),
            "co2": round(self.co2, 1),
            "temperature": round(self.temperature, 1),
            "humidity": round(self.humidity, 1),
            "water": round(self.water, 1),
            "alerts": len(self.alerts),
            "status": "operational" if self.oxygen > 75 else "critical"
        }
    
    def run(self):
        print("🌿 Life Support System")
        print("="*40)
        
        for _ in range(3):
            self.monitor_environment()
            time.sleep(0.5)
        
        if self.co2 > 2:
            self.activate_purification()
        
        print("\n📊 STATUS:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    life = LifeSupport()
    life.run()
