#!/usr/bin/env python3
"""
Astronaut AI Assistant - EVA Space Edition
"""

import time
import random
from datetime import datetime

class AstronautAI:
    def __init__(self):
        self.name = "EVA-Space"
        self.crew = []
        self.missions = []
        self.vitals = {}
        self.status = "ready"
    
    def add_crew_member(self, name):
        """Aggiunge un membro dell'equipaggio"""
        self.crew.append({
            "name": name,
            "role": "astronaut",
            "status": "active",
            "joined": datetime.now().isoformat()
        })
        print(f"👨‍🚀 Crew member {name} added")
        return True
    
    def check_vitals(self, crew_name):
        """Controlla i parametri vitali"""
        vitals = {
            "heart_rate": random.randint(60, 90),
            "oxygen_saturation": random.randint(95, 100),
            "blood_pressure": f"{random.randint(110, 130)}/{random.randint(70, 85)}",
            "temperature": round(random.uniform(36.0, 37.2), 1)
        }
        self.vitals[crew_name] = vitals
        print(f"🩺 Vitals for {crew_name}:")
        print(f"   ❤️ Heart Rate: {vitals['heart_rate']} bpm")
        print(f"   💨 O2: {vitals['oxygen_saturation']}%")
        print(f"   🩸 BP: {vitals['blood_pressure']}")
        print(f"   🌡️ Temp: {vitals['temperature']}°C")
        return vitals
    
    def start_mission(self, mission_name):
        """Avvia una missione"""
        mission = {
            "name": mission_name,
            "status": "active",
            "start": datetime.now().isoformat(),
            "crew": [c["name"] for c in self.crew]
        }
        self.missions.append(mission)
        print(f"🚀 Mission {mission_name} started!")
        return mission
    
    def process_xmr_payment(self, amount):
        """Processa pagamento XMR"""
        print(f"💰 Processing XMR payment: {amount} XMR")
        time.sleep(0.5)
        print("✅ Payment processed!")
        return {"status": "completed", "amount": amount}
    
    def get_status(self):
        return {
            "name": self.name,
            "status": self.status,
            "crew": len(self.crew),
            "missions": len(self.missions),
            "vitals": len(self.vitals)
        }
    
    def run(self):
        print(f"👨‍🚀 {self.name} activated!")
        print("="*40)
        
        self.add_crew_member("Cdr. Daniel")
        self.add_crew_member("Lt. Sarah")
        self.check_vitals("Cdr. Daniel")
        self.start_mission("Lunar Landing")
        self.process_xmr_payment(0.01)
        
        print("\n📊 STATUS:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    ai = AstronautAI()
    ai.run()
