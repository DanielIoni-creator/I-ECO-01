#!/usr/bin/env python3
"""
Space Station Core Module - MyZubster Orbital Base
"""

import time
import random
from datetime import datetime

class SpaceStationCore:
    def __init__(self):
        self.name = "MyZubster Space Station"
        self.status = "operational"
        self.crew = 0
        self.energy = 100
        self.oxygen = 100
        self.temperature = 20.0
        self.comms = {"S-band": "active", "UHF": "active"}
        self.modules = ["habitat", "laboratory", "control"]
    
    def deploy_module(self, module_name):
        """Installa un nuovo modulo"""
        print(f"🚀 Installazione modulo: {module_name}")
        self.modules.append(module_name)
        print(f"✅ Modulo {module_name} installato!")
        return True
    
    def check_life_support(self):
        """Controlla i sistemi di supporto vitale"""
        print("🌿 Controllo supporto vitale...")
        status = {
            "oxygen": self.oxygen,
            "temperature": self.temperature,
            "energy": self.energy,
            "status": "OK" if self.oxygen > 20 and self.energy > 10 else "CRITICAL"
        }
        print(f"   Ossigeno: {status['oxygen']}%")
        print(f"   Temperatura: {status['temperature']}°C")
        print(f"   Energia: {status['energy']}%")
        print(f"   Stato: {status['status']}")
        return status
    
    def add_crew(self, count):
        """Aggiunge membri dell'equipaggio"""
        self.crew += count
        print(f"👨‍🚀 {count} astronauti aggiunti. Equipaggio totale: {self.crew}")
        return self.crew
    
    def process_xmr_payment(self, amount):
        """Processa un pagamento XMR spaziale"""
        print(f"💰 Transazione XMR spaziale: {amount} XMR")
        # Simula elaborazione
        time.sleep(1)
        print("✅ Pagamento elaborato con successo!")
        return {"status": "completed", "amount": amount}
    
    def get_status(self):
        """Restituisce lo stato della stazione"""
        return {
            "name": self.name,
            "status": self.status,
            "crew": self.crew,
            "energy": self.energy,
            "oxygen": self.oxygen,
            "temperature": self.temperature,
            "modules": len(self.modules),
            "comms": self.comms
        }
    
    def run(self):
        """Avvia la stazione"""
        print(f"🛸 {self.name} attivata!")
        print("="*40)
        
        self.add_crew(3)
        self.deploy_module("solar_panels")
        self.deploy_module("research_lab")
        self.check_life_support()
        
        # Simula pagamento XMR
        self.process_xmr_payment(0.01)
        
        print("\n📊 STATO STAZIONE:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    station = SpaceStationCore()
    station.run()
