#!/usr/bin/env python3
"""
Fluffypony Voice Control - Comandi vocali per il robot
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue

class VoiceControl:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.command_queue = queue.Queue()
        self.is_listening = False
    
    def speak(self, text):
        """Risposta vocale"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        """Ascolta comandi vocali"""
        with sr.Microphone() as source:
            print("🎤 In ascolto...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                command = self.recognizer.recognize_google(audio, language='it-IT')
                print(f"📝 Riconosciuto: {command}")
                return command.lower()
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("❌ Non ho capito")
                return None
    
    def process_command(self, command):
        """Processa i comandi vocali"""
        if not command:
            return
        
        if "servi" in command or "drink" in command:
            self.speak("Servo subito il drink!")
            return "serve_drink"
        elif "luci" in command:
            self.speak("Accendo le luci!")
            return "lights_on"
        elif "balla" in command or "danza" in command:
            self.speak("Inizio a ballare!")
            return "dance"
        elif "stop" in command:
            self.speak("Fermo tutto!")
            return "stop"
        else:
            self.speak("Comando non riconosciuto")
            return None
    
    def start_listening(self):
        """Avvia il loop di ascolto"""
        self.is_listening = True
        self.speak("Ciao, sono Fluffypony! Sono pronto per i comandi vocali.")
        
        while self.is_listening:
            command = self.listen()
            if command:
                result = self.process_command(command)
                if result:
                    self.command_queue.put(result)
    
    def stop(self):
        """Ferma l'ascolto"""
        self.is_listening = False
        self.speak("Arrivederci!")

if __name__ == "__main__":
    vc = VoiceControl()
    try:
        vc.start_listening()
    except KeyboardInterrupt:
        vc.stop()
