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
    
    def clean(self, area):
        print(f"🧹 Pulizia di {area}...")
        cleaned = random.randint(10, 30)
        self.area_cleaned += cleaned
        self.battery -= random.randint(5, 15)
        print(f"   ✅ {cleaned}m² puliti")
        return cleaned
    
    def run(self):
        areas = ["soggiorno", "cucina", "camere", "bagno"]
        print(f"🤖 {self.name} avviato!")
        for area in areas:
            self.clean(area)
            time.sleep(0.5)
        print(f"\n✅ Pulizia completata!")
        print(f"   Area pulita: {self.area_cleaned}m²")
        print(f"   Batteria: {self.battery}%")

if __name__ == "__main__":
    cleaner = HeraCleaner()
    cleaner.run()
