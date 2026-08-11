from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import json
import os
import time
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# File di persistenza
DATA_FILE = 'payments.json'

# Configurazione wallet
MYZ_WALLET = 'myz_77d6ddd05bf30e8fef178ac1b5b5e112'
XMR_WALLET = 'xmr_641340aa6aa86029e833a5e5f5fb2b31'
PLATFORM_FEE = 2

# Memoria temporale di Pytho
temporal_memory = []
timeline_events = [
    {'event': '👽 Pytho creato', 'year': '2024', 'status': '✅ Completato'},
    {'event': '🌿 Primo orto botanico registrato', 'year': '2024', 'status': '✅ Completato'},
    {'event': '🏛️ Comune di Firenze si unisce', 'year': '2024', 'status': '✅ Completato'},
    {'event': '🚀 Gateway live su myzubster.com', 'year': '2024', 'status': '✅ Online'},
    {'event': '💳 Primo pagamento XMR e MYZ', 'year': '2024', 'status': '✅ Completato'},
    {'event': '🛸 Pytho viaggia nel tempo', 'year': '2124', 'status': '⏳ In corso...'},
    {'event': '🌌 Pytho diventa leggenda', 'year': '3000', 'status': '🌀 Previsione'}
]

def load_payments():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_payments(payments):
    with open(DATA_FILE, 'w') as f:
        json.dump(payments, f, indent=2)

payments = load_payments()

# ============================================
# ROTTE PYTHO TEMPORAL
# ============================================

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/temporal')
def temporal():
    return send_file('pytho-temporal.html')

@app.route('/temporal.css')
def temporal_css():
    return send_file('temporal.css')

@app.route('/temporal.js')
def temporal_js():
    return send_file('temporal.js')

# ROTTA: Viaggia nel tempo
@app.route('/api/pytho/timetravel', methods=['POST'])
def time_travel():
    data = request.json
    destination = data.get('destination', 'Orto Botanico di Roma')
    year = data.get('year', 2024)
    action = data.get('action', 'visita')
    
    travel_result = {
        'timestamp': datetime.now().isoformat(),
        'destination': destination,
        'year': year,
        'action': action,
        'status': '🛸 Viaggio temporale completato!',
        'pytho_message': '👽 Il tempo è un concetto umano...',
        'paradox_prevention': '✅ Attivo',
        'flux_capacitor': '1.21 GW ⚡'
    }
    
    temporal_memory.append({
        'event': f'Viaggio al {destination} ({year})',
        'timestamp': datetime.now().isoformat()
    })
    
    return jsonify({
        'success': True,
        'travel': travel_result,
        'timeline': temporal_memory
    })

# ROTTA: Timeline di Pytho
@app.route('/api/pytho/timeline')
def get_timeline():
    return jsonify({
        'success': True,
        'timeline': timeline_events,
        'temporal_memory': temporal_memory,
        'pytho_status': '🟢 Viaggiatore temporale attivo',
        'flux_capacitor_charge': '100%'
    })

# ROTTA: Stato flux capacitor
@app.route('/api/pytho/flux')
def flux_status():
    return jsonify({
        'success': True,
        'flux_capacitor': {
            'status': '🔋 Carico',
            'power': '1.21 GW',
            'charge': str(random.randint(1, 100)) + '%',
            'stability': '⚡ Stabile'
        },
        'pytho_message': '👽 Ritorno al futuro!'
    })

# ============================================
# ROTTE PAGAMENTI
# ============================================

@app.route('/api/dashboard')
def dashboard():
    total_xmr = sum(p['amount'] for p in payments if p.get('currency') == 'XMR' and p.get('status') == 'paid')
    total_myz = sum(p.get('net_amount', p['amount']) for p in payments if p.get('currency') == 'MYZ' and p.get('status') == 'paid')
    
    return jsonify({
        'success': True,
        'dashboard': {
            'total_payments': len(payments),
            'pending': len([p for p in payments if p.get('status') == 'pending']),
            'paid': len([p for p in payments if p.get('status') == 'paid']),
            'total_xmr': total_xmr,
            'total_myz': total_myz,
            'wallet_addresses': {
                'myz': MYZ_WALLET,
                'xmr': XMR_WALLET
            }
        }
    })

if __name__ == '__main__':
    print('🚀 MyZubster Gateway running on port 3001')
    print('👽 Pytho the Alien is watching!')
    print('⏳ Pytho Temporal attivo!')
    print('🛸 Macchina del tempo: http://localhost:3001/temporal')
    app.run(host='0.0.0.0', port=3001, debug=True)
