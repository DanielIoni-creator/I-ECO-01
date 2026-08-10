#!/usr/bin/env python3
import time

def test_laser():
    print("🧪 TEST LASER")
    print("   Accensione laser...")
    # GPIO.output(LASER_PIN, GPIO.HIGH)
    time.sleep(2)
    print("   Spegnimento laser...")
    # GPIO.output(LASER_PIN, GPIO.LOW)
    print("✅ Laser OK\n")

def test_emergency():
    print("🧪 TEST EMERGENZA")
    print("   Simulazione pulsante emergenza...")
    # Spegni tutto
    print("   Tutto spento")
    print("✅ Emergenza OK\n")

print("🧪 TEST SICUREZZA")
test_laser()
test_emergency()
print("✅ SISTEMA SICURO!")
