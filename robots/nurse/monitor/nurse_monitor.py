#!/usr/bin/env python3
"""
Nurse Monitor - Monitoraggio avanzato pazienti
"""

import time
import random

class NurseMonitor:
    def __init__(self):
        self.name = "Nurse Monitor"
        self.patients = []
        self.alerts = []
    
    def add_patient(self, patient_id):
        self.patients.append({
            "id": patient_id,
            "heart_rate": random.randint(60, 100),
            "temperature": round(random.uniform(36.0, 37.5), 1),
            "status": "stable"
        })
        print(f"🩺 Paziente {patient_id} aggiunto")
    
    def check_vitals(self, patient):
        hr = random.randint(60, 100)
        temp = round(random.uniform(36.0, 37.5), 1)
        patient["heart_rate"] = hr
        patient["temperature"] = temp
        
        if hr > 90:
            self.alerts.append(f"⚠️ Frequenza alta per {patient['id']}: {hr} bpm")
            patient["status"] = "critical"
        elif temp > 37.2:
            self.alerts.append(f"⚠️ Temperatura alta per {patient['id']}: {temp}°C")
            patient["status"] = "warning"
        else:
            patient["status"] = "stable"
        
        return patient
    
    def run(self):
        print(f"🏥 {self.name} avviato!")
        
        # Aggiungi pazienti
        for i in range(3):
            self.add_patient(f"P00{i+1}")
        
        print("\n📊 Monitoraggio in corso...")
        for patient in self.patients:
            self.check_vitals(patient)
            print(f"   {patient['id']}: {patient['heart_rate']} bpm, {patient['temperature']}°C ({patient['status']})")
            time.sleep(0.5)
        
        print(f"\n✅ Monitoraggio completato!")
        print(f"   Pazienti: {len(self.patients)}")
        print(f"   Allerte: {len(self.alerts)}")

if __name__ == "__main__":
    monitor = NurseMonitor()
    monitor.run()
