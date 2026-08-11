#!/usr/bin/env python3
"""
Interplanetary Communication Network
"""

import time
import random
from datetime import datetime

class InterplanetaryComm:
    def __init__(self):
        self.nodes = []
        self.messages = []
        self.delay_tolerance = True
    
    def deploy_node(self, location, type="relay"):
        """Installa un nodo di comunicazione"""
        node = {
            "id": f"NODE_{len(self.nodes)+1}",
            "location": location,
            "type": type,
            "status": "active",
            "latency": random.randint(100, 1000),
            "deployed": datetime.now().isoformat()
        }
        self.nodes.append(node)
        print(f"📡 Node deployed: {node['id']} at {location}")
        print(f"   Type: {type}, Latency: {node['latency']}ms")
        return node
    
    def send_message(self, from_node, to_node, content):
        """Invia un messaggio interplanetario"""
        message = {
            "id": f"MSG_{int(time.time())}",
            "from": from_node,
            "to": to_node,
            "content": content,
            "sent": datetime.now().isoformat(),
            "status": "delivered" if random.random() > 0.2 else "pending"
        }
        self.messages.append(message)
        print(f"📨 Message sent: {from_node} → {to_node}")
        print(f"   Content: {content[:50]}...")
        if self.delay_tolerance:
            print("   ⏳ Delay-tolerant routing enabled")
        return message
    
    def get_network_status(self):
        """Stato della rete"""
        active_nodes = sum(1 for n in self.nodes if n["status"] == "active")
        return {
            "nodes": len(self.nodes),
            "active_nodes": active_nodes,
            "messages": len(self.messages),
            "delayed": len([m for m in self.messages if m["status"] == "pending"]),
            "dtn_enabled": self.delay_tolerance
        }
    
    def run(self):
        print("🌍 Interplanetary Communication Network")
        print("="*40)
        
        self.deploy_node("Earth", "ground")
        self.deploy_node("Lunar Orbit", "relay")
        self.deploy_node("Mars", "satellite")
        
        self.send_message("Earth", "Mars", "Hello from MyZubster Space Station!")
        self.send_message("Lunar Orbit", "Earth", "Signal received, all systems nominal")
        
        print("\n📊 NETWORK STATUS:")
        status = self.get_network_status()
        for key, value in status.items():
            print(f"   {key}: {value}")

if __name__ == "__main__":
    network = InterplanetaryComm()
    network.run()
