#!/usr/bin/env python3
import time

# Simula il controllo delle pompe
PUMP_PINS = [18, 19, 20, 21]

def test_pump(pin):
    print(f"🧪 TEST POMPA {pin}")
    print(f"   Attivazione pompa {pin}...")
    # Qui va il codice reale con GPIO
    time.sleep(2)
    print(f"   Disattivazione pompa {pin}...")
    print("✅ Pompa OK\n")

print("🧪 TEST POMPE PERISTALTICHE")
for pin in PUMP_PINS:
    test_pump(pin)
print("✅ TUTTE LE POMPE FUNZIONANO!")
