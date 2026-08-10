#!/usr/bin/env python3
"""
Hera Security Robot - Robot di sicurezza avanzato
"""

import time
import random

class HeraSecurityRobot:
    def __init__(self):
        self.name = "Hera Security Robot"
        self.status = "idle"
        self.alerts = []
        self.detections = 0
    
    def patrol(self, area):
        print(f"🚨 Pattugliamento in {area}...")
        time.sleep(1)
        if random.random() < 0.1:
            self.alerts.append(f"⚠️ Movimento sospetto in {area}")
            self.detections += 1
            print(f"⚠️ Movimento sospetto rilevato!")
            return True
        print("✅ Area sicura")
        return False
    
    def run(self):
        areas = ["ingresso", "corridoio", "magazzino", "parcheggio"]
        print(f"🤖 {self.name} avviato!")
        for area in areas:
            self.patrol(area)
        print(f"\n✅ Pattugliamento completato!")
        print(f"   Rilevazioni: {self.detections}")
        print(f"   Allerte: {len(self.alerts)}")

if __name__ == "__main__":
    robot = HeraSecurityRobot()
    robot.run()
