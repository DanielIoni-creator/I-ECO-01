#!/usr/bin/env python3
"""
Smart Camera Module - Visione artificiale per i robot MyZubster
"""

import time
import random
from datetime import datetime

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
    print("✅ OpenCV disponibile")
except ImportError:
    OPENCV_AVAILABLE = False
    print("⚠️ OpenCV non disponibile - modalità mock")

class SmartCamera:
    def __init__(self, camera_id=0, use_yolo=False):
        self.camera_id = camera_id
        self.cap = None
        self.use_yolo = use_yolo
        self.running = False
        self.detected_objects = []
        print("📷 Smart Camera inizializzata")
    
    def start(self):
        if OPENCV_AVAILABLE:
            try:
                self.cap = cv2.VideoCapture(self.camera_id)
                if self.cap.isOpened():
                    self.running = True
                    print("📷 Camera avviata")
                    return True
            except:
                pass
        print("📷 Modalità mock attiva")
        return True
    
    def capture_frame(self):
        if OPENCV_AVAILABLE and self.cap and self.running:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return "mock_frame"
    
    def detect_faces(self, frame):
        return random.randint(0, 2)
    
    def detect_objects(self, frame):
        objects = ['person', 'cup', 'bottle', 'chair', 'glass']
        detected = []
        for _ in range(random.randint(0, 3)):
            detected.append({
                'class': random.choice(objects),
                'confidence': round(random.uniform(0.5, 0.95), 2)
            })
        return detected
    
    def process_frame(self, frame):
        return {
            'faces': self.detect_faces(frame),
            'objects': self.detect_objects(frame),
            'timestamp': datetime.now().isoformat()
        }
    
    def release(self):
        if OPENCV_AVAILABLE and self.cap:
            self.cap.release()
        self.running = False
        print("📷 Camera rilasciata")

class FluffyponyVision:
    def __init__(self):
        self.camera = SmartCamera(use_yolo=True)
    
    def check_glass(self):
        print("🔍 Verifica presenza bicchiere...")
        self.camera.start()
        frame = self.camera.capture_frame()
        results = self.camera.process_frame(frame)
        self.camera.release()
        for obj in results['objects']:
            if obj['class'] in ['cup', 'glass', 'bottle']:
                print(f"✅ Bicchiere rilevato: {obj['class']}")
                return True
        print("❌ Nessun bicchiere rilevato")
        return False
    
    def detect_person(self):
        self.camera.start()
        frame = self.camera.capture_frame()
        results = self.camera.process_frame(frame)
        self.camera.release()
        for obj in results['objects']:
            if obj['class'] in ['person', 'human']:
                print(f"✅ Persona rilevata: {obj['class']}")
                return True
        return False

class HeraSecurityVision:
    def __init__(self):
        self.camera = SmartCamera(use_yolo=True)
        self.intruders = []
    
    def check_intruder(self):
        print("🔍 Scansione area...")
        self.camera.start()
        frame = self.camera.capture_frame()
        results = self.camera.process_frame(frame)
        self.camera.release()
        if results['faces'] > 0:
            print(f"⚠️ {results['faces']} volti rilevati")
            if results['faces'] > 1:
                print("🚨 INTRUSO RILEVATO!")
                self.intruders.append({
                    'timestamp': datetime.now().isoformat(),
                    'faces': results['faces']
                })
                return True
        print("✅ Area sicura")
        return False
