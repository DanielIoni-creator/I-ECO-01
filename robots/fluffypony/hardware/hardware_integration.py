#!/usr/bin/env python3
"""
Hardware Integration per Fluffypony Laser
Supporto per Raspberry Pi, pompe e laser
"""

import time
import sys

class HardwareIntegration:
    def __init__(self):
        self.gpio_available = False
        self.GPIO = None
        self._init_gpio()
    
    def _init_gpio(self):
        """Inizializza GPIO se disponibile"""
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            GPIO.setmode(GPIO.BCM)
            self.gpio_available = True
            print("✅ GPIO disponibile")
        except ImportError:
            print("⚠️ RPi.GPIO non trovato - modalità mock")
            self.gpio_available = False
    
    def setup_pins(self, pump_pin=18, laser_pin=19):
        """Configura i pin GPIO"""
        if self.gpio_available:
            self.GPIO.setup(pump_pin, self.GPIO.OUT)
            self.GPIO.setup(laser_pin, self.GPIO.OUT)
            print(f"✅ Pin configurati: pompa={pump_pin}, laser={laser_pin}")
        else:
            print(f"⚠️ Mock: pin configurati {pump_pin}, {laser_pin}")
    
    def activate_pump(self, pin=18, duration=5):
        """Attiva pompa"""
        if self.gpio_available:
            self.GPIO.output(pin, self.GPIO.HIGH)
            time.sleep(duration)
            self.GPIO.output(pin, self.GPIO.LOW)
        else:
            # Mock
            for i in range(duration):
                print(f"   🔴 Pompa attiva... {i+1}s")
                time.sleep(1)
        return True
    
    def activate_laser(self, pin=19, duration=2):
        """Attiva laser"""
        if self.gpio_available:
            self.GPIO.output(pin, self.GPIO.HIGH)
            time.sleep(duration)
            self.GPIO.output(pin, self.GPIO.LOW)
        else:
            # Mock
            for i in range(duration):
                print(f"   🔴 LASER ATTIVO... {i+1}s")
                time.sleep(1)
        return True
    
    def cleanup(self):
        """Pulisce GPIO"""
        if self.gpio_available:
            self.GPIO.cleanup()
            print("🧹 GPIO pulito")

if __name__ == "__main__":
    hardware = HardwareIntegration()
    hardware.setup_pins()
    hardware.activate_pump(duration=3)
    hardware.activate_laser(duration=2)
    hardware.cleanup()
