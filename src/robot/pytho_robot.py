#!/usr/bin/env python3
"""
Pytho Robot Giardiniere - Modulo Principale
"""

import time
import json
import threading
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SensorData:
    temperature: float = 0.0
    humidity: float = 0.0
    soil_moisture: float = 0.0
    light: float = 0.0
    distance: float = 0.0

class PythoRobot:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sensors = SensorData()
        self.is_running = False
        self.thread = None
        
    def start(self):
        """Avvia il robot"""
        self.is_running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        print("🤖 Pytho Robot avviato!")
        
    def stop(self):
        """Ferma il robot"""
        self.is_running = False
        if self.thread:
            self.thread.join()
        print("🤖 Pytho Robot fermato")
        
    def _run(self):
        """Loop principale del robot"""
        while self.is_running:
            try:
                self._read_sensors()
                self._navigate()
                self._process_data()
                time.sleep(0.1)
            except Exception as e:
                print(f"Errore: {e}")
                
    def _read_sensors(self):
        """Legge i dati dai sensori"""
        # Simulazione lettura sensori
        self.sensors.temperature = 22.5
        self.sensors.humidity = 65
        self.sensors.soil_moisture = 45.2
        self.sensors.light = 800
        self.sensors.distance = 50
        print(f"📊 Sensori: {self.sensors}")
        
    def _navigate(self):
        """Gestisce la navigazione"""
        # Logica di navigazione
        print("🚗 Navigazione in corso...")
        
    def _process_data(self):
        """Processa i dati raccolti"""
        # Elaborazione dati
        data = {
            "sensors": {
                "temperature": self.sensors.temperature,
                "humidity": self.sensors.humidity,
                "soil_moisture": self.sensors.soil_moisture,
                "light": self.sensors.light,
                "distance": self.sensors.distance
            },
            "status": "active",
            "timestamp": time.time()
        }
        return data

if __name__ == "__main__":
    # Configurazione
    config = {
        "name": "Pytho",
        "speed": 0.5,
        "max_distance": 100
    }
    
    # Avvia robot
    robot = PythoRobot(config)
    try:
        robot.start()
        time.sleep(10)  # Esegue per 10 secondi
    except KeyboardInterrupt:
        robot.stop()
