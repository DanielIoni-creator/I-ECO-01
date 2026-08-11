#!/usr/bin/env python3
"""
Space Debris Tracker
"""

import time
import random
from datetime import datetime

class DebrisTracker:
    def __init__(self):
        self.debris = []
        self.alerts = []
        self.tracking_enabled = True
    
    def detect_debris(self, size="small"):
        """Rileva detriti spaziali"""
        debris = {
            "id": f"DEBRIS_{int(time.time())}",
            "size": size,
            "velocity": random.randint(5000, 15000),
            "altitude": random.randint(300, 2000),
            "trajectory": random.choice(["stable", "decaying", "collision_course"]),
            "detected": datetime.now().isoformat()
        }
        self.debris.append(debris)
        print(f"🛰️ Debris detected: {debris['id']} ({size})")
        print(f"   Velocity: {debris['velocity']} km/h")
        print(f"   Altitude: {debris['altitude']} km")
        
        if debris["trajectory"] == "collision_course":
            self.alert_collision(debris)
        
        return debris
    
    def alert_collision(self, debris):
        """Allerta collisione"""
        alert = {
            "id": f"ALERT_{int(time.time())}",
            "debris": debris["id"],
            "message": f"⚠️ Collision risk detected! Debris {debris['id']} on collision course",
            "timestamp": datetime.now().isoformat()
        }
        self.alerts.append(alert)
        print(f"🚨 COLLISION ALERT: {alert['message']}")
        return alert
    
    def calculate_trajectory(self, debris_id):
        """Calcola traiettoria"""
        for d in self.debris:
            if d["id"] == debris_id:
                print(f"📐 Calculating trajectory for {debris_id}...")
                time.sleep(0.5)
                result = {
                    "debris": debris_id,
                    "predicted_path": f"Altitude {d['altitude']-random.randint(1,10)}km",
                    "impact_window": random.randint(10, 60)
                }
                print(f"   Predicted path: {result['predicted_path']}")
                print(f"   Impact window: {result['impact_window']} min")
                return result
        return None
    
    def get_stats(self):
        """Statistiche"""
        return {
            "debris_tracked": len(self.debris),
            "alerts": len(self.alerts),
            "status": "active" if self.tracking_enabled else "inactive"
        }
    
    def run(self):
        print("🛰️ Space Debris Tracker")
        print("="*40)
        
        self.detect_debris("large")
        self.detect_debris("small")
        self.detect_debris("medium")
        
        if self.debris:
            self.calculate_trajectory(self.debris[0]["id"])
        
        print("\n📊 STATS:")
        stats = self.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    tracker = DebrisTracker()
    tracker.run()
