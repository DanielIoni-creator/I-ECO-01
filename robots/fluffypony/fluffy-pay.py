#!/usr/bin/env python3
import json, time, requests, RPi.GPIO as GPIO

XMR_RPC_URL = "http://localhost:18082/json_rpc"
PUMP_PIN = 18
LASER_PIN = 19
AMOUNT_XMR = 0.01

GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.setup(LASER_PIN, GPIO.OUT)

def check_xmr_payment(amount):
    try:
        payload = {"jsonrpc": "2.0", "id": "0", "method": "get_balance", "params": {"account_index": 0}}
        data = requests.post(XMR_RPC_URL, json=payload).json()
        return data.get("result", {}).get("balance", 0) / 1e12 >= amount
    except:
        return False

def serve_drink():
    print("🍹 Serving drink...")
    GPIO.output(PUMP_PIN, GPIO.HIGH)
    GPIO.output(LASER_PIN, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(PUMP_PIN, GPIO.LOW)
    GPIO.output(LASER_PIN, GPIO.LOW)
    print("✅ Drink served!")

def main():
    print("🤖 Fluffypony Laser Robot Barman")
    while True:
        if check_xmr_payment(AMOUNT_XMR):
            serve_drink()
        time.sleep(5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
