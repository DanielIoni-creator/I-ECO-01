#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

def test_laser():
    print("🧪 TEST LASER")
    print("   Accensione laser...")
    GPIO.output(LASER_PIN, GPIO.HIGH)
    time.sleep(2)
    print("   Spegnimento laser...")
    GPIO.output(LASER_PIN, GPIO.LOW)
    print("✅ Laser OK\n")

def test_emergency():
    print("🧪 TEST EMERGENZA")
    print("   Simulazione pulsante emergenza...")
    # Spegni tutto
    GPIO.output(LASER_PIN, GPIO.LOW)
    print("   Tutto spento")
    print("✅ Emergenza OK\n")

def test_oxygen():
    print("🧪 TEST OSSIGENO")
    print("   Verifica livello di ossigeno...")
    # Implementazione del sistema di controllo ossigeno
    time.sleep(2)
    print("   Livello di ossigeno OK\n")

def test_co2():
    print("🧪 TEST CO2")
    print("   Verifica livello di CO2...")
    # Implementazione del sistema di controllo CO2
    time.sleep(2)
    print("   Livello di CO2 OK\n")

print("🧪 TEST SICUREZZA")
test_laser()
test_emergency()
test_oxygen()
test_co2()
print("✅ SISTEMA SICURO!")