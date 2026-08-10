#!/usr/bin/env python3
"""
Robot Barman - MyZubster
Serve drink con pagamenti XMR
"""

import time

class RobotBarman:
    def __init__(self):
        self.drinks = {
            "1": "🍹 Mojito",
            "2": "🍸 Martini",
            "3": "🥃 Whiskey"
        }
    
    def show_menu(self):
        print("\n=== 🍸 ROBOT BARMAN ===")
        for key, drink in self.drinks.items():
            print(f"  {key}. {drink}")
        print("  0. Esci")
    
    def serve_drink(self, choice):
        if choice in self.drinks:
            print(f"\n🔧 Preparazione {self.drinks[choice]}...")
            time.sleep(2)
            print(f"✅ {self.drinks[choice]} servito! 🍹")
            return True
        return False
    
    def run(self):
        print("🤖 Robot Barman avviato!")
        while True:
            self.show_menu()
            choice = input("\nScegli un drink: ")
            if choice == "0":
                print("👋 Arrivederci!")
                break
            self.serve_drink(choice)

if __name__ == "__main__":
    barman = RobotBarman()
    barman.run()
