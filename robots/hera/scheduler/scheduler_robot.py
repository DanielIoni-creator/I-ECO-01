#!/usr/bin/env python3
"""
Hera Scheduler - Pianificazione robot di servizio
"""

import time
import json
from datetime import datetime

class HeraScheduler:
    def __init__(self):
        self.name = "Hera Scheduler"
        self.tasks = []
        self.schedule = {}
    
    def add_task(self, robot_name, task_type, time_slot, area=None):
        """Aggiunge un task programmato"""
        task = {
            "robot": robot_name,
            "type": task_type,
            "time": time_slot,
            "area": area,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        
        if time_slot not in self.schedule:
            self.schedule[time_slot] = []
        self.schedule[time_slot].append(task)
        
        print(f"📋 Task aggiunto: {robot_name} - {task_type} alle {time_slot}")
        return task
    
    def get_tasks_by_time(self, time_slot):
        """Restituisce i task per un orario specifico"""
        return self.schedule.get(time_slot, [])
    
    def get_all_tasks(self):
        """Restituisce tutti i task"""
        return self.tasks
    
    def get_pending_tasks(self):
        """Restituisce i task in attesa"""
        return [t for t in self.tasks if t["status"] == "pending"]
    
    def run_schedule(self):
        """Esegue la pianificazione"""
        print(f"\n🔄 {self.name} avvia pianificazione...")
        
        # Simula esecuzione dei task
        for task in self.get_pending_tasks():
            print(f"   ✅ Esecuzione: {task['robot']} - {task['type']}")
            task["status"] = "completed"
            time.sleep(0.3)
        
        print(f"\n✅ Pianificazione completata!")
        print(f"   Task eseguiti: {len([t for t in self.tasks if t['status'] == 'completed'])}")
        print(f"   Task rimanenti: {len(self.get_pending_tasks())}")
    
    def show_schedule(self):
        """Mostra la pianificazione"""
        if not self.schedule:
            print("📅 Nessuna pianificazione")
            return
        
        print("\n📅 PIANIFICAZIONE:")
        for time_slot, tasks in sorted(self.schedule.items()):
            print(f"   {time_slot}:")
            for task in tasks:
                status = "✅" if task["status"] == "completed" else "⏳"
                print(f"      {status} {task['robot']} - {task['type']}")

if __name__ == "__main__":
    scheduler = HeraScheduler()
    
    # Aggiungi task
    scheduler.add_task("Cleaner", "pulizia", "08:00", "soggiorno")
    scheduler.add_task("Gardener", "irrigazione", "10:00", "giardino")
    scheduler.add_task("Security", "pattugliamento", "14:00", "esterno")
    
    # Mostra pianificazione
    scheduler.show_schedule()
    
    # Esegui pianificazione
    scheduler.run_schedule()
    
    # Mostra pianificazione aggiornata
    scheduler.show_schedule()
