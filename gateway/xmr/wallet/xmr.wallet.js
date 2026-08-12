/**
 * 💰 Monero Wallet - Gestione Wallet XMR
 */

const MoneroWallet = require('monero-javascript');

class XMRWallet {
    constructor(config) {
        this.config = {
            rpcUrl: config.rpcUrl || 'http://localhost:18081',
            username: config.username || 'myzubster',
            password: config.password || 'pytho2026'
        };
        this.wallet = null;
    }

    // Inizializza il wallet
    async initialize() {
        try {
            this.wallet = await MoneroWallet.createWallet({
                networkType: 'stagenet', // Usa stagenet per test
                server: {
                    uri: this.config.rpcUrl,
                    username: this.config.username,
                    password: this.config.password
                }
            });
            console.log('✅ Wallet XMR inizializzato');
            return this.wallet;
        } catch (error) {
            console.error('❌ Errore inizializzazione wallet:', error);
            throw error;
        }
    }

    // Crea un nuovo indirizzo
    async createAddress() {
        try {
            const address = await this.wallet.getPrimaryAddress();
            return address;
        } catch (error) {
            console.error('❌ Errore creazione indirizzo:', error);
            throw error;
        }
    }

    // Ottieni il balance
    async getBalance() {
        try {
            const balance = await this.wallet.getBalance();
            return {
                unlocked: balance.unlockedBalance / 1e12, // Converti da atomic units a XMR
                total: balance.balance / 1e12
            };
        } catch (error) {
            console.error('❌ Errore recupero balance:', error);
            throw error;
        }
    }

    // Monitora transazioni
    async monitorTransactions() {
        try {
            const txs = await this.wallet.getTransactions();
            return txs.map(tx => ({
                id: tx.id,
                amount: tx.amount / 1e12,
                confirmations: tx.confirmations,
                timestamp: tx.timestamp,
                isOutgoing: tx.isOutgoing
            }));
        } catch (error) {
            console.error('❌ Errore monitoraggio transazioni:', error);
            throw error;
        }
    }

    // Invia pagamento
    async sendPayment(address, amount) {
        try {
            const result = await this.wallet.send({
                address: address,
                amount: amount * 1e12, // Converti a atomic units
                priority: 'normal'
            });
            return {
                txId: result.txHash,
                amount: amount,
                address: address,
                status: 'pending'
            };
        } catch (error) {
            console.error('❌ Errore invio pagamento:', error);
            throw error;
        }
    }
}

module.exports = { XMRWallet };
