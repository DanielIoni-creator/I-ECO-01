#!/usr/bin/env python3
"""
Hera Gardener - Robot giardiniere
"""

import time
import random
from datetime import datetime

class HeraGardener:
    def __init__(self):
        self.name = "Hera Gardener"
        self.plants = []
        self.water_level = 100
        self.fertilizer_level = 100
    
    def add_plant(self, name, type_plant, water_need=50):
        """Aggiunge una pianta al giardino"""
        plant = {
            "name": name,
            "type": type_plant,
            "water_need": water_need,
            "health": random.randint(60, 100),
            "watered": False,
            "fertilized": False
        }
        self.plants.append(plant)
        print(f"🌱 Aggiunta pianta: {name} ({type_plant})")
        return plant
    
    def check_plants(self):
        """Controlla lo stato delle piante"""
        print("\n🌿 Controllo piante...")
        for plant in self.plants:
            health = random.randint(60, 100)
            plant["health"] = health
            status = "✅" if health > 70 else "⚠️"
            print(f"   {status} {plant['name']}: salute {health}%")
        return self.plants
    
    def water_plants(self):
        """Irriga le piante"""
        print("\n💧 Irrigazione in corso...")
        for plant in self.plants:
            if plant["health"] < 70:
                print(f"   💦 Irrigazione {plant['name']}...")
                plant["watered"] = True
                plant["health"] = min(100, plant["health"] + 20)
                self.water_level -= 10
                time.sleep(0.3)
        print("✅ Irrigazione completata!")
        return True
    
    def fertilize_plants(self):
        """Fertilizza le piante"""
        print("\n🧪 Fertilizzazione in corso...")
        for plant in self.plants:
            if plant["health"] < 80:
                print(f"   🌿 Fertilizzazione {plant['name']}...")
                plant["fertilized"] = True
                plant["health"] = min(100, plant["health"] + 15)
                self.fertilizer_level -= 5
                time.sleep(0.3)
        print("✅ Fertilizzazione completata!")
        return True
    
    def get_garden_status(self):
        """Restituisce lo stato del giardino"""
        return {
            "plants": len(self.plants),
            "water_level": self.water_level,
            "fertilizer_level": self.fertilizer_level,
            "healthy_plants": len([p for p in self.plants if p["health"] > 70])
        }
    
    def run(self):
        """Esegue il robot giardiniere"""
        print(f"🌱 {self.name} avviato!")
        
        # Aggiungi piante
        self.add_plant("Rosa", "fiore", 60)
        self.add_plant("Basilico", "erba", 50)
        self.add_plant("Menta", "erba", 40)
        self.add_plant("Lavanda", "fiore", 30)
        
        # Controlla piante
        self.check_plants()
        
        # Irriga
        self.water_plants()
        
        # Fertilizza
        self.fertilize_plants()
        
        # Stato finale
        print("\n📊 STATO GIARDINO:")
        status = self.get_garden_status()
        print(f"   Piante: {status['plants']}")
        print(f"   Piante sane: {status['healthy_plants']}")
        print(f"   Acqua: {status['water_level']}%")
        print(f"   Fertilizzante: {status['fertilizer_level']}%")
        
        # Mostra piante
        print("\n🌿 PIANTE:")
        for plant in self.plants:
            status = "✅" if plant["health"] > 70 else "⚠️"
            print(f"   {status} {plant['name']}: salute {plant['health']}%")

if __name__ == "__main__":
    gardener = HeraGardener()
    gardener.run()
