#!/usr/bin/env python3
"""
Satellite Communication System
"""

import time
import random
from datetime import datetime

class SatelliteComms:
    def __init__(self):
        self.satellites = []
        self.ground_stations = ["Mission Control", "Ground Station 1"]
        self.comms_log = []
    
    def deploy_satellite(self, name, orbit="LEO"):
        """Lancia un satellite"""
        satellite = {
            "name": name,
            "orbit": orbit,
            "status": "active",
            "last_contact": datetime.now().isoformat()
        }
        self.satellites.append(satellite)
        print(f"🛰️ Satellite {name} deployed in {orbit} orbit")
        return satellite
    
    def send_data(self, satellite_name, data):
        """Invia dati a un satellite"""
        print(f"📡 Sending data to {satellite_name}: {data[:50]}...")
        time.sleep(0.5)
        self.comms_log.append({
            "satellite": satellite_name,
            "data": data[:100],
            "timestamp": datetime.now().isoformat()
        })
        print(f"✅ Data sent to {satellite_name}")
        return True
    
    def receive_data(self, satellite_name):
        """Riceve dati da un satellite"""
        print(f"📡 Receiving data from {satellite_name}...")
        time.sleep(0.5)
        data = {
            "satellite": satellite_name,
            "telemetry": {
                "battery": random.randint(80, 100),
                "temperature": random.randint(-20, 40),
                "orbit": "LEO"
            },
            "timestamp": datetime.now().isoformat()
        }
        print(f"✅ Data received from {satellite_name}")
        return data
    
    def process_xmr_transaction(self, amount):
        """Processa una transazione XMR via satellite"""
        print(f"💰 Processing XMR transaction via satellite: {amount} XMR")
        time.sleep(1)
        print("✅ Transaction completed!")
        return {"status": "completed", "amount": amount}
    
    def get_status(self):
        """Stato del sistema"""
        return {
            "satellites": len(self.satellites),
            "ground_stations": self.ground_stations,
            "comms_log": len(self.comms_log)
        }
    
    def run(self):
        print("🛰️ Satellite Communication System")
        print("="*40)
        
        # Deploy satellites
        self.deploy_satellite("MyZubster-1", "LEO")
        self.deploy_satellite("MyZubster-2", "MEO")
        
        # Send data
        self.send_data("MyZubster-1", "Hello from MyZubster Space Station!")
        
        # Receive data
        data = self.receive_data("MyZubster-1")
        
        # Process payment
        self.process_xmr_transaction(0.01)
        
        print("\n📊 STATUS:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    comms = SatelliteComms()
    comms.run()
