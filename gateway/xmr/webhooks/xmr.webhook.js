/**
 * 🔔 XMR Webhooks - Gestione Webhook
 */

const express = require('express');
const router = express.Router();
const { XMRPayments } = require('../payments/xmr.payments');

const payments = new XMRPayments();

// Webhook per ricezione pagamenti
router.post('/webhook/xmr/payment', async (req, res) => {
    try {
        const { paymentId, status, txHash, confirmations } = req.body;
        
        console.log('📥 Webhook XMR ricevuto:', { paymentId, status, txHash, confirmations });
        
        // Aggiorna lo stato del pagamento
        const payment = payments.updatePaymentStatus(paymentId, status);
        if (!payment) {
            return res.status(404).json({
                success: false,
                error: 'Pagamento non trovato'
            });
        }
        
        // Se il pagamento è completato, aggiorna il saldo dell'utente
        if (status === 'completed' && confirmations >= 10) {
            // Qui si potrebbe aggiornare il saldo dell'utente
            console.log('✅ Pagamento completato:', paymentId);
        }
        
        res.json({
            success: true,
            message: 'Webhook processato con successo',
            data: payment
        });
    } catch (error) {
        console.error('❌ Errore webhook:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Webhook per conferme
router.post('/webhook/xmr/confirmation', async (req, res) => {
    try {
        const { paymentId, confirmations, txHash } = req.body;
        
        console.log('📥 Conferma XMR ricevuta:', { paymentId, confirmations, txHash });
        
        // Aggiorna le conferme del pagamento
        const payment = payments.payments.find(p => p.id === paymentId);
        if (payment) {
            payment.confirmations = confirmations;
            payment.txHash = txHash;
            payment.updatedAt = new Date().toISOString();
            payments.savePayments();
        }
        
        res.json({
            success: true,
            message: 'Conferma processata con successo'
        });
    } catch (error) {
        console.error('❌ Errore conferma:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

module.exports = router;
