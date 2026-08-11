#!/usr/bin/env python3
"""
Lunar Rover Explorer
"""

import time
import random
from datetime import datetime

class LunarRover:
    def __init__(self):
        self.name = "MyZubster Lunar Rover"
        self.position = (0, 0)
        self.battery = 100
        self.samples = []
        self.status = "idle"
    
    def move(self, direction, distance):
        """Muove il rover"""
        print(f"🚀 Moving {direction} for {distance}m...")
        if direction == "north":
            self.position = (self.position[0], self.position[1] + distance)
        elif direction == "south":
            self.position = (self.position[0], self.position[1] - distance)
        elif direction == "east":
            self.position = (self.position[0] + distance, self.position[1])
        elif direction == "west":
            self.position = (self.position[0] - distance, self.position[1])
        
        self.battery -= random.randint(1, 5)
        print(f"📍 New position: {self.position}")
        return self.position
    
    def collect_sample(self, sample_type):
        """Raccoglie un campione"""
        print(f"🔬 Collecting {sample_type} sample...")
        sample = {
            "type": sample_type,
            "location": self.position,
            "timestamp": datetime.now().isoformat()
        }
        self.samples.append(sample)
        print(f"✅ Sample collected: {sample_type}")
        return sample
    
    def take_photo(self):
        """Scatta una foto"""
        print("📷 Taking photo...")
        time.sleep(0.5)
        photo = {
            "timestamp": datetime.now().isoformat(),
            "location": self.position,
            "type": "lunar_surface"
        }
        print("✅ Photo taken!")
        return photo
    
    def process_xmr_payment(self, amount):
        """Processa pagamento XMR"""
        print(f"💰 Processing XMR payment: {amount} XMR")
        time.sleep(0.5)
        print("✅ Payment processed!")
        return {"status": "completed", "amount": amount}
    
    def get_status(self):
        """Stato del rover"""
        return {
            "name": self.name,
            "position": self.position,
            "battery": self.battery,
            "samples": len(self.samples),
            "status": self.status
        }
    
    def run(self):
        print(f"🚀 {self.name}")
        print("="*40)
        
        # Esplorazione
        self.move("north", 10)
        self.collect_sample("rock")
        self.move("east", 5)
        self.collect_sample("soil")
        self.take_photo()
        self.move("south", 8)
        self.collect_sample("mineral")
        
        # Pagamento
        self.process_xmr_payment(0.01)
        
        print("\n📊 STATUS:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    rover = LunarRover()
    rover.run()
