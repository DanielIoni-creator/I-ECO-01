#!/usr/bin/env python3
"""
Music Robot - Robot musicista
"""

import time
import random
from datetime import datetime

class MusicRobot:
    def __init__(self):
        self.name = "MusicBot"
        self.notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
        self.rhythms = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
        self.songs = []
        self.played_notes = []
        self.bpm = 120
    
    def play_note(self, note, duration):
        """Suona una nota musicale"""
        print(f"🎵 Suona {note} (durata: {duration}s)")
        self.played_notes.append({
            'note': note,
            'duration': duration,
            'timestamp': datetime.now().isoformat()
        })
        time.sleep(duration)
        return True
    
    def play_melody(self, melody):
        """Suona una melodia"""
        print(f"🎶 Esecuzione melodia: {melody['name']}")
        
        for note in melody['notes']:
            note_name = note['note']
            duration = note.get('duration', 0.3)
            self.play_note(note_name, duration)
        
        print("✅ Melodia completata!")
        return True
    
    def create_melody(self, length=8):
        """Crea una melodia casuale"""
        melody = {
            'name': f'Melodia_{len(self.songs) + 1}',
            'notes': []
        }
        
        for _ in range(length):
            note = {
                'note': random.choice(self.notes),
                'duration': random.choice(self.rhythms)
            }
            melody['notes'].append(note)
        
        self.songs.append(melody)
        print(f"🎵 Melodia creata: {melody['name']}")
        return melody
    
    def set_bpm(self, bpm):
        """Imposta il tempo (BPM)"""
        self.bpm = bpm
        print(f"🎵 Tempo impostato: {bpm} BPM")
        return bpm
    
    def get_stats(self):
        """Statistiche del robot"""
        return {
            'songs_created': len(self.songs),
            'notes_played': len(self.played_notes),
            'bpm': self.bpm
        }
    
    def run_demo(self):
        """Demo del robot musicista"""
        print(f"🎵 {self.name} avviato!")
        print("🎹 Robot musicista")
        
        # Imposta tempo
        self.set_bpm(140)
        
        # Crea e suona melodie
        for _ in range(3):
            melody = self.create_melody(6)
            self.play_melody(melody)
            time.sleep(0.5)
        
        # Mostra statistiche
        print("\n📊 STATISTICHE:")
        stats = self.get_stats()
        print(f"   Melodie create: {stats['songs_created']}")
        print(f"   Note suonate: {stats['notes_played']}")
        print(f"   BPM: {stats['bpm']}")

if __name__ == "__main__":
    robot = MusicRobot()
    robot.run_demo()
