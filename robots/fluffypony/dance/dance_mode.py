#!/usr/bin/env python3
"""
Fluffypony Dance Mode - Movimenti sincronizzati con musica
"""

import time
import random
import threading

class DanceMode:
    def __init__(self):
        self.dancing = False
        self.moves = [
            "twist", "wave", "spin", "jump", "sway",
            "robot", "moonwalk", "c-walk", "glide"
        ]
    
    def start_dance(self):
        """Avvia la modalità ballo"""
        self.dancing = True
        print("🕺 Fluffypony inizia a ballare!")
        threading.Thread(target=self._dance_loop).start()
    
    def stop_dance(self):
        """Ferma il ballo"""
        self.dancing = False
        print("💃 Fluffypony si ferma!")
    
    def _dance_loop(self):
        """Loop del ballo"""
        while self.dancing:
            move = random.choice(self.moves)
            print(f"🎵 Movimento: {move}")
            time.sleep(random.uniform(0.5, 1.5))
    
    def sync_with_music(self, bpm=120):
        """Sincronizza con la musica"""
        interval = 60 / bpm
        print(f"🎵 Sincronizzato a {bpm} BPM")
        return interval

if __name__ == "__main__":
    dance = DanceMode()
    try:
        dance.start_dance()
        input("Premi Invio per fermare...")
        dance.stop_dance()
    except KeyboardInterrupt:
        dance.stop_dance()
