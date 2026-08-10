#!/usr/bin/env python3
"""
Nurse Assistant Robot - Assistente per infermieri
"""

import time
import random
import json
from datetime import datetime

class NurseAssistant:
    def __init__(self):
        self.name = "NurseBot"
        self.status = "idle"
        self.patient_id = None
        self.tasks = []
        self.medications = []
        self.deliveries = []
        self.battery = 100
    
    def load_patient(self, patient_id):
        """Carica i dati del paziente"""
        self.patient_id = patient_id
        print(f"🩺 Caricamento paziente {patient_id}...")
        
        # Simula dati paziente
        patient_data = {
            'id': patient_id,
            'name': f"Paziente {patient_id}",
            'room': f"Stanza {random.randint(100, 200)}",
            'medications': [
                {'name': 'Paracetamolo', 'dosage': '500mg', 'time': '08:00'},
                {'name': 'Antibiotico', 'dosage': '250mg', 'time': '14:00'}
            ]
        }
        self.patient_data = patient_data
        print(f"✅ Paziente {patient_id} caricato: {patient_data['name']}")
        return patient_data
    
    def deliver_medication(self, medication):
        """Consegna farmaci al paziente"""
        print(f"💊 Consegna farmaco: {medication['name']} {medication['dosage']}...")
        time.sleep(1)
        
        delivery = {
            'medication': medication['name'],
            'dosage': medication['dosage'],
            'patient': self.patient_id,
            'delivered_at': datetime.now().isoformat(),
            'status': 'delivered'
        }
        self.deliveries.append(delivery)
        print(f"✅ Farmaco consegnato: {medication['name']}")
        return delivery
    
    def check_vitals(self):
        """Controlla i parametri vitali del paziente"""
        print(f"📊 Controllo parametri vitali per paziente {self.patient_id}...")
        time.sleep(0.5)
        
        vitals = {
            'heart_rate': random.randint(65, 95),
            'spo2': random.randint(95, 100),
            'temperature': round(random.uniform(36.2, 37.2), 1),
            'blood_pressure': f"{random.randint(110, 130)}/{random.randint(70, 85)}"
        }
        
        print(f"   ❤️ Frequenza: {vitals['heart_rate']} bpm")
        print(f"   💨 SpO2: {vitals['spo2']}%")
        print(f"   🌡️ Temperatura: {vitals['temperature']}°C")
        print(f"   🩸 Pressione: {vitals['blood_pressure']} mmHg")
        return vitals
    
    def navigate_to_room(self, room):
        """Naviga verso la stanza del paziente"""
        print(f"🧭 Navigando verso {room}...")
        time.sleep(1)
        print(f"📍 Arrivato in {room}")
        return True
    
    def add_task(self, task_type, description):
        """Aggiunge un task alla lista"""
        task = {
            'id': len(self.tasks) + 1,
            'type': task_type,
            'description': description,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        self.tasks.append(task)
        print(f"📋 Task aggiunto: {task_type} - {description}")
        return task
    
    def process_medications(self):
        """Processa le somministrazioni di farmaci"""
        if not self.patient_data:
            print("❌ Nessun paziente caricato")
            return
        
        print(f"\n💊 Processando farmaci per {self.patient_data['name']}...")
        
        for med in self.patient_data.get('medications', []):
            self.deliver_medication(med)
            time.sleep(0.5)
    
    def get_status(self):
        """Restituisce lo stato del robot"""
        return {
            'name': self.name,
            'status': self.status,
            'patient': self.patient_id,
            'battery': self.battery,
            'tasks_pending': len([t for t in self.tasks if t['status'] == 'pending']),
            'deliveries': len(self.deliveries)
        }
    
    def run(self):
        """Loop principale del robot"""
        print(f"🏥 {self.name} avviato!")
        
        # Simula assistenza a un paziente
        self.load_patient("P001")
        self.navigate_to_room("Stanza 101")
        self.check_vitals()
        self.process_medications()
        
        print("\n📊 STATO ATTUALE:")
        status = self.get_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    robot = NurseAssistant()
    try:
        robot.run()
    except KeyboardInterrupt:
        print("\n🛑 Robot fermato")
