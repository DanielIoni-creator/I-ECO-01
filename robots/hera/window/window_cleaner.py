#!/usr/bin/env python3
"""
Hera Window Cleaner - Robot lavavetri
"""

import time
import random
from datetime import datetime

class WindowCleaner:
    def __init__(self):
        self.name = "Hera WindowCleaner"
        self.status = "idle"
        self.battery = 100
        self.windows_cleaned = 0
        self.surface_cleaned = 0  # m²
        self.safety_active = True
    
    def attach_to_window(self):
        """Si attacca alla superficie del vetro"""
        print("🧲 Attacco al vetro...")
        time.sleep(1)
        print("✅ Attacco riuscito!")
        return True
    
    def clean_surface(self, size_m2):
        """Pulisce una superficie di vetro"""
        if self.battery < 20:
            print("⚠️ Batteria bassa, impossibile pulire")
            return False
        
        print(f"🧹 Pulizia superficie di {size_m2} m²...")
        
        # Simula pulizia
        time.sleep(2)
        self.windows_cleaned += 1
        self.surface_cleaned += size_m2
        self.battery -= random.randint(5, 15)
        
        print(f"✅ Superficie pulita! {size_m2} m²")
        return True
    
    def navigate_vertical(self, direction):
        """Naviga verticalmente sul vetro"""
        print(f"⬆️ Navigazione verticale: {direction}")
        time.sleep(0.5)
        return True
    
    def check_safety(self):
        """Verifica i sistemi di sicurezza"""
        if not self.safety_active:
            print("⚠️ SISTEMA DI SICUREZZA DISATTIVATO!")
            return False
        
        print("🛡️ Sistemi di sicurezza OK")
        return True
    
    def activate_safety(self):
        """Attiva i sistemi di sicurezza"""
        self.safety_active = True
        print("🛡️ Sistemi di sicurezza attivati")
        return True
    
    def get_stats(self):
        """Statistiche del robot"""
        return {
            'windows_cleaned': self.windows_cleaned,
            'surface_cleaned': self.surface_cleaned,
            'battery': self.battery,
            'status': self.status
        }
    
    def run(self):
        """Simula pulizia vetri"""
        print(f"🧹 {self.name} avviato!")
        self.check_safety()
        self.attach_to_window()
        
        # Simula pulizia di più vetri
        windows = [
            {'size': 4.5, 'floor': 3},
            {'size': 3.2, 'floor': 4},
            {'size': 5.0, 'floor': 2}
        ]
        
        for window in windows:
            print(f"\n🪟 Pulizia vetro piano {window['floor']}...")
            self.clean_surface(window['size'])
            self.navigate_vertical("su")
            time.sleep(0.5)
        
        print("\n📊 STATISTICHE:")
        stats = self.get_stats()
        print(f"   Vetri puliti: {stats['windows_cleaned']}")
        print(f"   Superficie pulita: {stats['surface_cleaned']} m²")
        print(f"   Batteria: {stats['battery']}%")

if __name__ == "__main__":
    cleaner = WindowCleaner()
    try:
        cleaner.run()
    except KeyboardInterrupt:
        print("\n🛑 Robot fermato")
