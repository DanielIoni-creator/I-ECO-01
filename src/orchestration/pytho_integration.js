/**
 * Pytho Fisico - Sistema Integrato Completo
 * Orchestrazione di tutti i componenti
 */

const express = require('express');
const WebSocket = require('ws');
const mqtt = require('mqtt');
const { spawn } = require('child_process');

// Configurazione
const config = {
  mqtt: {
    host: 'mqtt.myzubster.com',
    port: 1883
  },
  robot: {
    enabled: true,
    api: 'http://localhost:5000'
  },
  sensors: {
    enabled: true,
    topics: ['pytho/sensors/#']
  },
  display: {
    enabled: true,
    port: 3002
  },
  lights: {
    enabled: true,
    serial: '/dev/ttyUSB0'
  }
};

class PythoSystem {
  constructor() {
    this.components = {};
    this.status = {};
    this.mqttClient = null;
    this.wsServer = null;
    this.isRunning = false;
  }

  async start() {
    console.log('🔗 Avvio sistema integrato Pytho...');
    this.isRunning = true;
    await this.initMQTT();
    this.initWebSocket();
    await this.startComponents();
    console.log('✅ Sistema Pytho integrato avviato!');
  }

  async initMQTT() {
    return new Promise((resolve) => {
      this.mqttClient = mqtt.connect(`mqtt://${config.mqtt.host}`);
      this.mqttClient.on('connect', () => {
        console.log('📡 Connesso a MQTT');
        this.mqttClient.subscribe('pytho/sensors/#');
        resolve();
      });
      this.mqttClient.on('message', (topic, message) => {
        this.handleSensorData(topic, message.toString());
      });
    });
  }

  initWebSocket() {
    const wss = new WebSocket.Server({ port: 8080 });
    this.wsServer = wss;
    wss.on('connection', (ws) => {
      console.log('🖥️ Client WebSocket connesso');
      ws.on('message', (message) => {
        const data = JSON.parse(message);
        this.handleCommand(data);
      });
      ws.send(JSON.stringify({ type: 'status', data: this.status }));
    });
    console.log('🔌 WebSocket server avviato su porta 8080');
  }

  async startComponents() {
    if (config.robot.enabled) {
      const robot = spawn('python3', ['src/robot/pytho_robot.py']);
      robot.stdout.on('data', (data) => {
        console.log(`🤖 Robot: ${data}`);
      });
      this.components.robot = robot;
    }
    if (config.display.enabled) {
      const display = spawn('node', ['src/display/display_server.js']);
      display.stdout.on('data', (data) => {
        console.log(`🖥️ Display: ${data}`);
      });
      this.components.display = display;
    }
    console.log('✅ Tutti i componenti avviati');
  }

  handleSensorData(topic, message) {
    const value = parseFloat(message);
    const sensor = topic.split('/').pop();
    this.status[sensor] = value;
    this.wsServer.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'sensor',
          sensor: sensor,
          value: value,
          timestamp: Date.now()
        }));
      }
    });
  }

  handleCommand(data) {
    switch(data.command) {
      case 'set_mode':
        this.setMode(data.mode);
        break;
      case 'get_status':
        this.sendStatus();
        break;
      default:
        console.log(`Comando sconosciuto: ${data.command}`);
    }
  }

  setMode(mode) {
    console.log(`🎯 Modalità impostata: ${mode}`);
    this.status.mode = mode;
    if (this.mqttClient) {
      this.mqttClient.publish('pytho/command/mode', mode);
    }
  }

  sendStatus() {
    this.wsServer.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(JSON.stringify({
          type: 'status',
          data: this.status
        }));
      }
    });
  }

  stop() {
    console.log('⏹️ Arresto sistema Pytho...');
    this.isRunning = false;
    Object.values(this.components).forEach(proc => {
      if (proc.kill) proc.kill();
    });
    if (this.mqttClient) {
      this.mqttClient.end();
    }
    console.log('✅ Sistema arrestato');
  }
}

const system = new PythoSystem();
system.start().catch(console.error);

process.on('SIGINT', () => {
  system.stop();
  process.exit();
});

module.exports = system;
