#!/usr/bin/env python3
"""
Art Robot - Robot per disegno e arte
"""

import time
import random
from datetime import datetime

class ArtRobot:
    def __init__(self):
        self.name = "ArtBot"
        self.canvas = []
        self.colors = ['#FF0000', '#00FF00', '#0000FF', '#FF9900', '#9900FF']
        self.current_color = '#000000'
        self.pen_down = False
        self.position = (0, 0)
    
    def draw_pixel(self, x, y, color):
        """Disegna un pixel"""
        print(f"🎨 Disegna pixel a ({x}, {y}) con colore {color}")
        self.canvas.append({
            'x': x,
            'y': y,
            'color': color,
            'timestamp': datetime.now().isoformat()
        })
        return True
    
    def draw_line(self, x1, y1, x2, y2):
        """Disegna una linea tra due punti"""
        print(f"📏 Disegna linea da ({x1},{y1}) a ({x2},{y2})")
        
        # Simula disegno di una linea
        steps = max(abs(x2-x1), abs(y2-y1))
        for i in range(steps + 1):
            x = x1 + (x2-x1) * i // steps
            y = y1 + (y2-y1) * i // steps
            self.draw_pixel(x, y, self.current_color)
            time.sleep(0.1)
        
        return True
    
    def change_color(self, color):
        """Cambia il colore corrente"""
        self.current_color = color
        print(f"🎨 Colore cambiato: {color}")
        return True
    
    def pen_up(self):
        """Alza la penna"""
        self.pen_down = False
        print("🖊️ Penna alzata")
        return True
    
    def pen_down(self):
        """Abbassa la penna"""
        self.pen_down = True
        print("🖊️ Penna abbassata")
        return True
    
    def create_art(self, style):
        """Crea un'opera d'arte in uno stile specifico"""
        print(f"🎨 Creazione arte in stile {style}...")
        
        if style == 'abstract':
            for _ in range(10):
                x = random.randint(0, 100)
                y = random.randint(0, 100)
                color = random.choice(self.colors)
                self.draw_pixel(x, y, color)
        
        elif style == 'geometric':
            shapes = [
                (10, 10, 50, 10, 50, 50, 10, 50),  # Quadrato
                (70, 10, 90, 10, 80, 40),  # Triangolo
                (20, 70, 80, 70, 80, 90, 20, 90)  # Rettangolo
            ]
            for shape in shapes:
                for i in range(0, len(shape)-3, 2):
                    self.draw_line(shape[i], shape[i+1], shape[i+2], shape[i+3])
        
        print("✅ Opera completata!")
        return self.canvas
    
    def get_stats(self):
        """Statistiche del robot"""
        return {
            'total_pixels': len(self.canvas),
            'current_color': self.current_color,
            'position': self.position,
            'pen_down': self.pen_down
        }
    
    def run_demo(self):
        """Demo del robot artistico"""
        print(f"🎨 {self.name} avviato!")
        print("🖌️ Robot per disegno e arte")
        
        # Crea opere d'arte
        self.change_color('#FF0000')
        self.create_art('abstract')
        
        self.change_color('#0000FF')
        self.create_art('geometric')
        
        # Mostra statistiche
        print("\n📊 STATISTICHE:")
        stats = self.get_stats()
        print(f"   Pixel disegnati: {stats['total_pixels']}")
        print(f"   Colore corrente: {stats['current_color']}")

if __name__ == "__main__":
    robot = ArtRobot()
    robot.run_demo()
