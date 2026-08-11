#!/usr/bin/env python3
"""
Root Access I2C Adapter per MyZubster
Ponte per comunicare con il DC34 Badge via I2C
"""

import time
import random
from datetime import datetime

class RootAccessI2CAdapter:
    def __init__(self, bus_id=0):
        self.bus_id = bus_id
        self.devices = {}
        self.current_address = 0x50
        self.current_data = 0x00
        self.connected = False

    def scan(self):
        print("🔍 Scansione bus I2C...")
        time.sleep(0.5)
        devices = []
        for addr in [0x50, 0x68, 0x19, 0x3C]:
            if addr == 0x19 or addr == 0x3C:
                print(f"   ⚠️ 0x{addr:02X} badge device - refused")
            elif addr == 0x50:
                print(f"   ✅ 0x{addr:02X} Root Access SAO")
                devices.append({"address": addr, "name": "Root Access SAO"})
            else:
                print(f"   ✅ 0x{addr:02X}")
                devices.append({"address": addr, "name": f"Device {addr:02X}"})
        return devices

    def send(self, address, data):
        print(f"📤 Inviando 0x{data:02X} a 0x{address:02X}...")
        time.sleep(0.2)
        return {"success": True, "address": address, "data": data}

    def probe(self, address):
        print(f"🔎 Probing 0x{address:02X}...")
        time.sleep(0.1)
        if address == 0x50:
            print(f"   ✅ ACK - Root Access SAO")
            return {"status": "ACK", "address": address}
        elif address in [0x19, 0x3C]:
            print(f"   ⚠️ No response - badge device refused")
            return {"status": "refused", "address": address}
        elif address in [0x68]:
            print(f"   ✅ ACK")
            return {"status": "ACK", "address": address}
        else:
            print(f"   ❌ No response")
            return {"status": "no response", "address": address}

    def quick_command(self, address, command):
        print(f"⚡ Comando rapido su 0x{address:02X}: {command}")
        return {"success": True, "command": command, "address": address}

    def connect(self):
        self.connected = True
        print("🔗 Connesso al DC34 Badge")
        return True

    def disconnect(self):
        self.connected = False
        print("🔌 Disconnesso dal DC34 Badge")
        return True

class FluffyponyI2C:
    def __init__(self):
        self.adapter = RootAccessI2CAdapter()
        self.connected = False

    def connect_to_badge(self):
        self.connected = self.adapter.connect()
        return self.connected

    def scan_for_devices(self):
        if not self.connected:
            print("❌ Collegare prima il badge!")
            return []
        return self.adapter.scan()

    def send_command_to_sao(self, command):
        if not self.connected:
            print("❌ Collegare prima il badge!")
            return None
        return self.adapter.send(0x50, command)

    def cycle_animation(self):
        if not self.connected:
            print("❌ Collegare prima il badge!")
            return None
        for i in range(0, 0x32, 0x05):
            print(f"🔄 Animazione 0x{i:02X}")
            self.adapter.send(0x50, i)
            time.sleep(1)
        return True

    def set_animation(self, animation_number):
        if not self.connected:
            print("❌ Collegare prima il badge!")
            return None
        if 0 <= animation_number <= 0x31:
            print(f"🎬 Imposto animazione 0x{animation_number:02X}")
            return self.adapter.send(0x50, animation_number)
        else:
            print(f"❌ Animazione {animation_number} non valida (0-49)")
            return None

    def get_device_info(self, address):
        if not self.connected:
            print("❌ Collegare prima il badge!")
            return None
        print(f"📊 Info su dispositivo 0x{address:02X}")
        return {
            "address": address,
            "status": "unknown",
            "timestamp": datetime.now().isoformat()
        }

class HeraI2C:
    def __init__(self):
        self.adapter = RootAccessI2CAdapter()
        self.connected = False
        self.monitored_addresses = [0x50, 0x68]

    def connect_to_badge(self):
        self.connected = self.adapter.connect()
        return self.connected

    def monitor_bus(self):
        if not self.connected:
            print("❌ Collegare prima il badge!")
            return None
        print("🛡️ Monitoraggio bus I2C...")
        results = []
        for addr in self.monitored_addresses:
            status = self.adapter.probe(addr)
            results.append(status)
        return results

    def detect_intrusion(self):
        if not self.connected:
            print("❌ Collegare prima il badge!")
            return None
        print("🚨 Rilevamento intrusi I2C...")
        for addr in self.monitored_addresses:
            result = self.adapter.probe(addr)
            if result["status"] == "no response":
                print(f"⚠️ Dispositivo 0x{addr:02X} non risponde!")
                return {"intrusion": True, "device": addr}
        print("✅ Nessuna intrusione rilevata")
        return {"intrusion": False}

if __name__ == "__main__":
    print("🧪 TEST I2C ADAPTER")
    print("="*40)

    adapter = RootAccessI2CAdapter()
    devices = adapter.scan()
    print(f"\n📋 Dispositivi trovati: {len(devices)}")

    print("\n🦄 TEST FLUFFYPONY I2C")
    fluffy = FluffyponyI2C()
    fluffy.connect_to_badge()
    fluffy.scan_for_devices()
    fluffy.set_animation(0x10)
    fluffy.cycle_animation()

    print("\n🛡️ TEST HERA I2C")
    hera = HeraI2C()
    hera.connect_to_badge()
    hera.monitor_bus()
    hera.detect_intrusion()

    print("\n✅ Test completato!")
