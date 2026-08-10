#!/usr/bin/env python3
"""
FLUFFYPONY LASER ROBOT
Robot che serve drink con pagamenti XMR e effetti laser
"""

import time
import json
import random
import threading
from datetime import datetime

# ============================================
# CONFIGURAZIONE
# ============================================

CONFIG = {
    "pumps": {
        "pin": 18,
        "duration": 5,
        "flow_rate": 0.5  # ml/s
    },
    "laser": {
        "pin": 19,
        "color": "red",
        "intensity": 0.8
    },
    "xmr": {
        "price_per_drink": 0.01,
        "wallet": "45M4DW1ug8bdQowWpxucTpgsfjLbVxbYaAra79VewmBobuuhgqTjyD4R3DzpqLM2veiphcB16n24qN1QbLg3y2PYGK3Qkoe"
    },
    "drinks": {
        "mojito": {"name": "🍹 Mojito", "ingredients": ["rum", "menta", "lime"], "time": 5},
        "martini": {"name": "🍸 Martini", "ingredients": ["gin", "vermouth"], "time": 4},
        "whiskey": {"name": "🥃 Whiskey", "ingredients": ["whiskey"], "time": 3}
    }
}

# ============================================
# CLASSE FLUFFYPONY
# ============================================

class FluffyponyLaser:
    def __init__(self, config=None):
        self.config = config or CONFIG
        self.status = "idle"
        self.drinks_served = 0
        self.xmr_received = 0
        self.is_running = False
        
        # Inizializza GPIO (mock per test)
        self.gpio_initialized = False
        self._init_gpio()
    
    def _init_gpio(self):
        """Inizializza GPIO (mock per test)"""
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.config["pumps"]["pin"], GPIO.OUT)
            GPIO.setup(self.config["laser"]["pin"], GPIO.OUT)
            self.gpio_initialized = True
            print("✅ GPIO inizializzato")
        except ImportError:
            print("⚠️ RPi.GPIO non trovato - modalità mock")
            self.GPIO = None
            self.gpio_initialized = False
    
    def check_payment(self, amount):
        """Verifica pagamento XMR"""
        print(f"💰 Verifica pagamento di {amount} XMR...")
        # In produzione: chiamata a wallet-rpc
        # Mock: simula pagamento dopo 3 secondi
        time.sleep(2)
        return True
    
    def activate_pump(self, duration=5):
        """Attiva pompa peristaltica"""
        print(f"🔧 Attivazione pompa per {duration} secondi...")
        if self.gpio_initialized:
            self.GPIO.output(self.config["pumps"]["pin"], self.GPIO.HIGH)
            time.sleep(duration)
            self.GPIO.output(self.config["pumps"]["pin"], self.GPIO.LOW)
        else:
            # Mock
            for i in range(duration):
                print(f"   🔴 Pompa attiva... {i+1}s")
                time.sleep(1)
        print("✅ Pompa disattivata")
    
    def activate_laser(self, duration=2):
        """Attiva laser"""
        print(f"🔴 Attivazione laser per {duration} secondi...")
        if self.gpio_initialized:
            self.GPIO.output(self.config["laser"]["pin"], self.GPIO.HIGH)
            time.sleep(duration)
            self.GPIO.output(self.config["laser"]["pin"], self.GPIO.LOW)
        else:
            # Mock
            for i in range(duration):
                print(f"   🔴 LASER ATTIVO... {i+1}s")
                time.sleep(1)
        print("⚫ Laser disattivato")
    
    def serve_drink(self, drink_name="mojito"):
        """Servi un drink"""
        drink = self.config["drinks"].get(drink_name, self.config["drinks"]["mojito"])
        
        print(f"\n🍹 Preparazione {drink['name']}...")
        print(f"   📋 Ingredienti: {', '.join(drink['ingredients'])}")
        
        # 1. Attiva pompa
        self.activate_pump(drink["time"])
        
        # 2. Attiva laser (effetto speciale)
        self.activate_laser(2)
        
        # 3. Aggiorna statistiche
        self.drinks_served += 1
        self.xmr_received += self.config["xmr"]["price_per_drink"]
        
        print(f"✅ {drink['name']} servito! 🎉")
        return True
    
    def show_status(self):
        """Mostra stato del robot"""
        print("\n" + "="*40)
        print("🤖 FLUFFYPONY LASER ROBOT")
        print("="*40)
        print(f"   Stato: {self.status}")
        print(f"   Drink serviti: {self.drinks_served}")
        print(f"   XMR incassati: {self.xmr_received:.4f} XMR")
        print(f"   Prezzo per drink: {self.config['xmr']['price_per_drink']} XMR")
        print("="*40)
    
    def run_demo(self):
        """Esegue una demo completa"""
        print("🚀 AVVIO DEMO FLUFFYPONY LASER")
        print("="*40)
        
        # Mostra menu
        self.show_status()
        
        # Simula 3 clienti
        drinks = ["mojito", "martini", "whiskey"]
        for i, drink in enumerate(drinks, 1):
            print(f"\n👤 Cliente #{i}: ordina {drink}")
            
            # Verifica pagamento
            if self.check_payment(self.config["xmr"]["price_per_drink"]):
                print("✅ Pagamento ricevuto!")
                self.serve_drink(drink)
            else:
                print("❌ Pagamento fallito")
        
        # Statistiche finali
        self.status = "completed"
        self.show_status()
        print("\n🎉 DEMO COMPLETATA!")
    
    def interactive_mode(self):
        """Modalità interattiva"""
        print("🤖 FLUFFYPONY LASER ROBOT - MODALITÀ INTERATTIVA")
        print("Comandi: menu, status, laser, serve <drink>, exit")
        
        while True:
            cmd = input("\n> ").strip().lower()
            
            if cmd == "exit":
                print("👋 Spegnimento...")
                break
            elif cmd == "menu":
                print("\n🍹 MENU DRINK:")
                for key, drink in self.config["drinks"].items():
                    print(f"   {key}: {drink['name']} ({drink['time']}s)")
            elif cmd == "status":
                self.show_status()
            elif cmd == "laser":
                self.activate_laser(3)
            elif cmd.startswith("serve "):
                drink = cmd.split(" ", 1)[1]
                if drink in self.config["drinks"]:
                    if self.check_payment(self.config["xmr"]["price_per_drink"]):
                        self.serve_drink(drink)
                    else:
                        print("❌ Pagamento fallito")
                else:
                    print(f"❌ Drink '{drink}' non trovato")
            else:
                print("❌ Comando non riconosciuto")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    robot = FluffyponyLaser()
    
    # Avvia modalità interattiva
    robot.interactive_mode()
    
    # Oppure esegui demo
    # robot.run_demo()
