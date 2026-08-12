/**
 * 💰 XMR Payments - Gestione Pagamenti
 */

const { XMRWallet } = require('../wallet/xmr.wallet');
const fs = require('fs');
const path = require('path');

const PAYMENTS_FILE = path.join(__dirname, '../../../payments.json');

class XMRPayments {
    constructor() {
        this.wallet = new XMRWallet({});
        this.payments = [];
        this.loadPayments();
    }

    // Carica i pagamenti dal file
    loadPayments() {
        try {
            if (fs.existsSync(PAYMENTS_FILE)) {
                const data = fs.readFileSync(PAYMENTS_FILE, 'utf8');
                this.payments = JSON.parse(data);
            }
        } catch (error) {
            console.error('❌ Errore caricamento pagamenti:', error);
            this.payments = [];
        }
    }

    // Salva i pagamenti
    savePayments() {
        try {
            fs.writeFileSync(PAYMENTS_FILE, JSON.stringify(this.payments, null, 2));
        } catch (error) {
            console.error('❌ Errore salvataggio pagamenti:', error);
        }
    }

    // Crea un nuovo pagamento
    async createPayment(userId, amount, currency = 'XMR') {
        try {
            const address = await this.wallet.createAddress();
            
            const payment = {
                id: `xmr_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
                userId,
                amount,
                currency,
                address,
                status: 'pending',
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString()
            };
            
            this.payments.push(payment);
            this.savePayments();
            
            return payment;
        } catch (error) {
            console.error('❌ Errore creazione pagamento:', error);
            throw error;
        }
    }

    // Verifica lo stato di un pagamento
    async checkPayment(paymentId) {
        try {
            const payment = this.payments.find(p => p.id === paymentId);
            if (!payment) {
                throw new Error('Pagamento non trovato');
            }
            
            // Qui si dovrebbe interrogare il wallet per verificare la transazione
            // Per ora simuliamo con un controllo fittizio
            
            return {
                id: payment.id,
                status: payment.status,
                amount: payment.amount,
                address: payment.address,
                confirmations: payment.confirmations || 0
            };
        } catch (error) {
            console.error('❌ Errore verifica pagamento:', error);
            throw error;
        }
    }

    // Aggiorna lo stato di un pagamento
    updatePaymentStatus(paymentId, status) {
        const payment = this.payments.find(p => p.id === paymentId);
        if (payment) {
            payment.status = status;
            payment.updatedAt = new Date().toISOString();
            this.savePayments();
            return payment;
        }
        return null;
    }

    // Ottieni tutti i pagamenti di un utente
    getUserPayments(userId) {
        return this.payments.filter(p => p.userId === userId);
    }

    // Converti XMR in MYZ
    convertXMRtoMYZ(xmrAmount) {
        // Tasso di cambio fittizio: 1 XMR = 1000 MYZ
        const rate = 1000;
        return xmrAmount * rate;
    }

    // Converti MYZ in XMR
    convertMYZtoXMR(myzAmount) {
        const rate = 1000;
        return myzAmount / rate;
    }
}

module.exports = { XMRPayments };
