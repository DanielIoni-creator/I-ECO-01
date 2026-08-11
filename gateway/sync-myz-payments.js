#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const axios = require('axios');

// Configurazione
const PAYMENTS_FILE = path.join(__dirname, 'payments.json');
const MYZ_API_URL = process.env.MYZUBSTER_API_URL || 'http://localhost:3000';
const MYZ_API_KEY = process.env.MYZUBSTER_API_KEY || '';

async function syncMyzPayments() {
    console.log('🔄 Avvio sincronizzazione pagamenti MYZ...');
    
    try {
        // Leggi i pagamenti
        if (!fs.existsSync(PAYMENTS_FILE)) {
            console.log('❌ File payments.json non trovato');
            return;
        }
        
        const data = fs.readFileSync(PAYMENTS_FILE, 'utf8');
        const payments = JSON.parse(data);
        
        // Filtra pagamenti MYZ non sincronizzati
        const myzPayments = payments.filter(p => 
            p.currency === 'MYZ' && 
            p.status === 'paid' && 
            !p.synced_to_myz
        );
        
        if (myzPayments.length === 0) {
            console.log('✅ Nessun pagamento MYZ da sincronizzare');
            return;
        }
        
        console.log(`📊 Trovati ${myzPayments.length} pagamenti MYZ da sincronizzare`);
        
        for (const payment of myzPayments) {
            try {
                console.log(`🔄 Sincronizzazione ${payment.id}...`);
                
                // Invia a MyZubster
                const response = await axios.post(`${MYZ_API_URL}/api/payments/confirm`, {
                    payment_id: payment.id,
                    tag_id: payment.tag_id,
                    amount: payment.net_amount || payment.amount,
                    currency: 'MYZ',
                    fee: payment.fee || 0
                }, {
                    headers: {
                        'Authorization': `Bearer ${MYZ_API_KEY}`,
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.data.success) {
                    payment.synced_to_myz = true;
                    payment.synced_at = new Date().toISOString();
                    console.log(`✅ Pagamento ${payment.id} sincronizzato`);
                }
                
            } catch (error) {
                console.error(`❌ Errore sincronizzazione ${payment.id}:`, error.message);
                if (error.response) {
                    console.error(`   Status: ${error.response.status}`);
                    console.error(`   Data: ${JSON.stringify(error.response.data)}`);
                }
            }
        }
        
        // Salva i pagamenti aggiornati
        fs.writeFileSync(PAYMENTS_FILE, JSON.stringify(payments, null, 2));
        console.log('✅ Sincronizzazione completata');
        
    } catch (error) {
        console.error('❌ Errore durante la sincronizzazione:', error);
    }
}

// Esegui
syncMyzPayments();
