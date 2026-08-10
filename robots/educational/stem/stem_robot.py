#!/usr/bin/env python3
"""
STEM Robot - Robot educativo per coding
"""

import time
import random
from datetime import datetime

class STEMRobot:
    def __init__(self):
        self.name = "STEMBot"
        self.position = (0, 0)
        self.direction = "north"
        self.moves = 0
        self.programs = []
        self.students = []
    
    def move_forward(self, steps=1):
        """Muove il robot in avanti"""
        print(f"🚶 Movimento avanti di {steps} passi...")
        self.position = (self.position[0] + steps, self.position[1])
        self.moves += 1
        return self.position
    
    def turn(self, direction):
        """Gira il robot"""
        print(f"🔄 Gira a {direction}")
        self.direction = direction
        return self.direction
    
    def run_program(self, program):
        """Esegue un programma di istruzioni"""
        print(f"📋 Esecuzione programma: {program['name']}")
        
        for instruction in program['instructions']:
            if instruction['type'] == 'move':
                self.move_forward(instruction.get('steps', 1))
            elif instruction['type'] == 'turn':
                self.turn(instruction['direction'])
            time.sleep(0.5)
        
        print(f"✅ Programma completato!")
        return self.position
    
    def add_student(self, student_name):
        """Aggiunge uno studente alla classe"""
        self.students.append({
            'name': student_name,
            'joined': datetime.now().isoformat(),
            'programs': []
        })
        print(f"👨‍🎓 Studente {student_name} aggiunto!")
        return True
    
    def get_stats(self):
        """Statistiche del robot"""
        return {
            'position': self.position,
            'direction': self.direction,
            'moves': self.moves,
            'students': len(self.students),
            'programs': len(self.programs)
        }
    
    def run_demo(self):
        """Demo del robot educativo"""
        print(f"🤖 {self.name} avviato!")
        print("📚 Robot educativo per coding e robotica")
        
        # Aggiungi studenti
        self.add_student("Alice")
        self.add_student("Bob")
        self.add_student("Charlie")
        
        # Crea un programma di esempio
        program = {
            'name': 'Percorso Base',
            'instructions': [
                {'type': 'move', 'steps': 3},
                {'type': 'turn', 'direction': 'east'},
                {'type': 'move', 'steps': 2},
                {'type': 'turn', 'direction': 'south'}
            ]
        }
        self.programs.append(program)
        
        # Esegui il programma
        print(f"\n📋 Esecuzione programma esempio:")
        self.run_program(program)
        
        # Mostra statistiche
        print("\n📊 STATISTICHE:")
        stats = self.get_stats()
        print(f"   Posizione: {stats['position']}")
        print(f"   Direzione: {stats['direction']}")
        print(f"   Movimenti: {stats['moves']}")
        print(f"   Studenti: {stats['students']}")
        print(f"   Programmi: {stats['programs']}")

if __name__ == "__main__":
    robot = STEMRobot()
    robot.run_demo()
