#!/usr/bin/env python3
"""
Fluffypony Web Server - Controllo robot da remoto
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import json
import time

app = Flask(__name__)

# Stato del robot
robot_status = {
    "status": "idle",
    "drinks_served": 0,
    "xmr_earned": 0,
    "last_drink": None
}

@app.route('/')
def index():
    return render_template('index.html', status=robot_status)

@app.route('/api/status')
def get_status():
    return jsonify(robot_status)

@app.route('/api/serve/<drink>')
def serve_drink(drink):
    if drink not in ['mojito', 'martini', 'whiskey']:
        return jsonify({"error": "Drink non valido"}), 400
    
    robot_status["status"] = "serving"
    robot_status["last_drink"] = drink
    
    # Simula servizio
    time.sleep(2)
    robot_status["drinks_served"] += 1
    robot_status["xmr_earned"] += 0.01
    robot_status["status"] = "idle"
    
    return jsonify({"success": True, "drink": drink})

@app.route('/api/laser')
def activate_laser():
    robot_status["status"] = "laser"
    time.sleep(1)
    robot_status["status"] = "idle"
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
