#!/usr/bin/env python3
"""
Vital Signs Monitor - Monitoraggio parametri vitali
"""

import random

class VitalSignsMonitor:
    def __init__(self):
        self.patient = None
        self.vitals = {}
    
    def start_monitoring(self, patient_id):
        self.patient = patient_id
        print(f"🩺 Monitoraggio avviato per paziente {patient_id}")
        return True
    
    def read_vitals(self):
        self.vitals = {
            "heart_rate": random.randint(60, 100),
            "spo2": random.randint(95, 100),
            "temperature": round(random.uniform(36.0, 37.5), 1)
        }
        return self.vitals
    
    def check_alerts(self):
        alerts = []
        if self.vitals["heart_rate"] > 90:
            alerts.append("⚠️ Frequenza cardiaca alta")
        if self.vitals["spo2"] < 95:
            alerts.append("⚠️ Saturazione bassa")
        if self.vitals["temperature"] > 37.2:
            alerts.append("⚠️ Febbre")
        return alerts
    
    def run(self):
        print("🤖 Vital Signs Monitor avviato!")
        self.start_monitoring("P001")
        vitals = self.read_vitals()
        alerts = self.check_alerts()
        print(f"❤️ Frequenza: {vitals['heart_rate']} bpm")
        print(f"💨 SpO2: {vitals['spo2']}%")
        print(f"🌡️ Temperatura: {vitals['temperature']}°C")
        if alerts:
            print("🚨 ALLARMI:")
            for alert in alerts:
                print(f"   {alert}")

if __name__ == "__main__":
    monitor = VitalSignsMonitor()
    monitor.run()
