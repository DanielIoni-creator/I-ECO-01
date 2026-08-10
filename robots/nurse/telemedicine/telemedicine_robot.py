#!/usr/bin/env python3
"""
Telemedicine Robot - Visite mediche remote
"""

import time
import random
import json
from datetime import datetime

class TelemedicineRobot:
    def __init__(self):
        self.name = "TeleMedBot"
        self.status = "idle"
        self.patient_id = None
        self.session = None
        self.medical_records = []
        self.video_quality = "HD"
    
    def start_consultation(self, patient_id, doctor_id):
        """Avvia una consultazione remota"""
        print(f"🩺 Avvio consultazione per paziente {patient_id} con dottore {doctor_id}...")
        time.sleep(1)
        
        self.patient_id = patient_id
        self.session = {
            'patient': patient_id,
            'doctor': doctor_id,
            'started_at': datetime.now().isoformat(),
            'status': 'active'
        }
        print(f"✅ Consultazione avviata!")
        print(f"   📹 Video quality: {self.video_quality}")
        return self.session
    
    def measure_vitals(self):
        """Misura i parametri vitali a distanza"""
        print(f"📊 Misurazione parametri vitali per paziente {self.patient_id}...")
        time.sleep(0.5)
        
        vitals = {
            'heart_rate': random.randint(60, 100),
            'spo2': random.randint(95, 100),
            'temperature': round(random.uniform(36.0, 37.5), 1),
            'blood_pressure': f"{random.randint(110, 140)}/{random.randint(70, 90)}",
            'timestamp': datetime.now().isoformat()
        }
        
        self.medical_records.append(vitals)
        
        print(f"   ❤️ Frequenza: {vitals['heart_rate']} bpm")
        print(f"   💨 SpO2: {vitals['spo2']}%")
        print(f"   🌡️ Temperatura: {vitals['temperature']}°C")
        print(f"   🩸 Pressione: {vitals['blood_pressure']} mmHg")
        return vitals
    
    def transmit_data(self, data):
        """Trasmette i dati al medico"""
        print(f"📤 Trasmissione dati al medico...")
        time.sleep(0.5)
        print(f"✅ Dati trasmessi: {len(data)} parametri")
        return True
    
    def receive_prescription(self):
        """Riceve la prescrizione dal medico"""
        print(f"📥 Ricezione prescrizione dal medico...")
        time.sleep(0.5)
        
        prescription = {
            'medications': [
                {'name': 'Farmaco A', 'dosage': '500mg', 'frequency': '2x al giorno'},
                {'name': 'Farmaco B', 'dosage': '250mg', 'frequency': '1x al giorno'}
            ],
            'notes': 'Riposo e idratazione',
            'doctor': 'Dr. Rossi',
            'issued_at': datetime.now().isoformat()
        }
        print(f"✅ Prescrizione ricevuta: {len(prescription['medications'])} farmaci")
        return prescription
    
    def end_consultation(self):
        """Termina la consultazione"""
        if self.session:
            self.session['status'] = 'completed'
            self.session['ended_at'] = datetime.now().isoformat()
            print(f"✅ Consultazione terminata!")
            print(f"   Durata: {self.session['ended_at']}")
            return True
        return False
    
    def get_patient_summary(self):
        """Restituisce un riepilogo del paziente"""
        return {
            'patient_id': self.patient_id,
            'records': self.medical_records,
            'consultations': self.session
        }
    
    def run(self):
        """Simula una consultazione telemedicina"""
        print(f"🏥 {self.name} avviato!")
        print("📡 Connessione alla rete telemedicina...")
        time.sleep(0.5)
        
        # Simula consultazione
        self.start_consultation("P002", "D001")
        
        print("\n📊 Misurazione parametri:")
        vitals = self.measure_vitals()
        self.transmit_data(vitals)
        
        print("\n📋 Prescrizione:")
        prescription = self.receive_prescription()
        for med in prescription['medications']:
            print(f"   💊 {med['name']} {med['dosage']} - {med['frequency']}")
        
        self.end_consultation()
        
        print("\n📊 RIEPILOGO CONSULTAZIONE:")
        summary = self.get_patient_summary()
        print(f"   Paziente: {summary['patient_id']}")
        print(f"   Records: {len(summary['records'])}")
        print(f"   Status: {summary['consultations']['status']}")

if __name__ == "__main__":
    robot = TelemedicineRobot()
    try:
        robot.run()
    except KeyboardInterrupt:
        print("\n🛑 Robot fermato")
