#!/usr/bin/env python3
"""
Hera Cleaner - Robot aspirapolvere avanzato
"""

import time
import random

class HeraCleaner:
    def __init__(self):
        self.name = "Hera Cleaner"
        self.area_cleaned = 0
        self.battery = 100
        self.deep_clean_mode = False
    
    def enable_deep_clean(self):
        self.deep_clean_mode = True
        print(f"🔄 Modalità Pulizia Profonda attivata per {self.name}")

    def recognize_obstacles(self):
        obstacles = ["sedia", "tavolo", "scarpe", "giocattolo", "cavo"]
        detected = random.sample(obstacles, k=random.randint(0, 2))
        if detected:
            print(f"   👁️ AI: Ostacoli rilevati: {', '.join(detected)}")
        return detected

    def detect_dirt(self):
        dirt_level = random.randint(1, 10)
        has_stain = random.choice([True, False])
        if has_stain:
            print("   🦠 AI: Macchia ostinata rilevata! Richiesto lavaggio intensivo.")
        return dirt_level, has_stain

    def optimize_route(self, area):
        print(f"   🗺️ AI: Calcolo percorso ottimizzato per {area}...")
        time.sleep(0.2)
        return "percorso a zig-zag intelligente"

    def clean(self, area):
        print(f"🧹 Pulizia di {area}...")
        self.optimize_route(area)
        self.recognize_obstacles()
        dirt_level, has_stain = self.detect_dirt()
        
        base_clean = random.randint(10, 30)
        multiplier = 1.5 if self.deep_clean_mode else 1.0
        cleaned = int(base_clean * multiplier)
        
        self.area_cleaned += cleaned
        self.battery -= random.randint(5, 15)
        
        if has_stain and self.deep_clean_mode:
            print("   ✨ Macchia rimossa con successo in modalità profonda!")
            
        print(f"   ✅ {cleaned}m² puliti (Livello sporco: {dirt_level}/10)")
        return cleaned
    
    def run(self):
        areas = ["soggiorno", "cucina", "camere", "bagno"]
        print(f"🤖 {self.name} avviato con Intelligenza Artificiale!")
        self.enable_deep_clean()
        for area in areas:
            self.clean(area)
            time.sleep(0.5)
        print(f"\n✅ Pulizia completata!")
        print(f"   Area totale pulita: {self.area_cleaned}m²")
        print(f"   Batteria rimanente: {self.battery}%")

if __name__ == "__main__":
    cleaner = HeraCleaner()
    cleaner.run()
