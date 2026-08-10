#!/usr/bin/env python3
"""
Nurse Monitor - Monitoraggio avanzato pazienti
"""

import time
import random
import datetime

class MedicalSensor:
    def read(self):
        return {
            "heart_rate": random.randint(50, 110),
            "temperature": round(random.uniform(35.5, 38.5), 1),
            "spo2": random.randint(90, 100),
            "blood_pressure": f"{random.randint(110, 140)}/{random.randint(70, 90)}"
        }

class NurseMonitor:
    def __init__(self):
        self.name = "Nurse Monitor"
        self.patients = []
        self.alerts = []
        self.sensor = MedicalSensor()
    
    def add_patient(self, patient_id):
        self.patients.append({
            "id": patient_id,
            "vitals": self.sensor.read(),
            "status": "stable"
        })
        print(f"🩺 Paziente {patient_id} aggiunto al sistema con sensori medici attivi")
    
    def check_vitals(self, patient):
        vitals = self.sensor.read()
        patient["vitals"] = vitals
        hr = vitals["heart_rate"]
        temp = vitals["temperature"]
        spo2 = vitals["spo2"]
        
        # Allarmi Intelligenti
        critical = False
        if hr > 100 or hr < 60:
            self.alerts.append(f"⚠️ [ALLARME INTELLIGENTE] Frequenza anomala per {patient['id']}: {hr} bpm")
            critical = True
        if temp > 37.5:
            self.alerts.append(f"⚠️ [ALLARME INTELLIGENTE] Temperatura alta per {patient['id']}: {temp}°C")
            critical = True
        if spo2 < 95:
            self.alerts.append(f"⚠️ [ALLARME INTELLIGENTE] SpO2 basso per {patient['id']}: {spo2}%")
            critical = True
            
        patient["status"] = "critical" if critical else "stable"
        return patient
    
    def generate_report(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n📄 --- REPORT AUTOMATICO ---")
        print(f"Generato il: {timestamp}")
        print(f"Pazienti monitorati: {len(self.patients)}")
        print(f"Allarmi totali generati: {len(self.alerts)}")
        print("Stato Pazienti:")
        for p in self.patients:
            print(f" - {p['id']}: {p['status'].upper()}")
        print("----------------------------\n")

    def display_dashboard(self):
        print("\n📊 --- REAL-TIME PATIENT DASHBOARD ---")
        for patient in self.patients:
            v = patient["vitals"]
            print(f"[{patient['id']}] Stato: {patient['status'].upper()}")
            print(f"   ❤️ HR: {v['heart_rate']} bpm | 🌡️ Temp: {v['temperature']}°C | 💨 SpO2: {v['spo2']}% | 🩸 PA: {v['blood_pressure']}")
        print("--------------------------------------\n")

    def run(self):
        print(f"🏥 {self.name} avviato con monitoraggio avanzato!")
        
        # Integrazione Sensori Medici
        print("\n🔌 Inizializzazione sensori medici...")
        time.sleep(0.5)
        
        for i in range(3):
            self.add_patient(f"P00{i+1}")
        
        print("\n📈 Inizio monitoraggio continuo in tempo reale...")
        for _ in range(2): # 2 cicli di monitoraggio per simulazione
            for patient in self.patients:
                self.check_vitals(patient)
            self.display_dashboard()
            time.sleep(1)
        
        self.generate_report()
        print(f"✅ Turno completato per {self.name}!")

if __name__ == "__main__":
    monitor = NurseMonitor()
    monitor.run()
