/**
 * 📱 Push Manager - Gestione Notifiche Push
 */

class PushManager {
    constructor() {
        this.subscriptions = new Map();
    }

    // Registra un dispositivo per le notifiche push
    registerDevice(userId, subscription) {
        if (!this.subscriptions.has(userId)) {
            this.subscriptions.set(userId, []);
        }
        this.subscriptions.get(userId).push(subscription);
        console.log(`📱 Dispositivo registrato per utente ${userId}`);
    }

    // Rimuovi un dispositivo
    unregisterDevice(userId, subscription) {
        if (this.subscriptions.has(userId)) {
            const subs = this.subscriptions.get(userId);
            const index = subs.indexOf(subscription);
            if (index > -1) {
                subs.splice(index, 1);
            }
            if (subs.length === 0) {
                this.subscriptions.delete(userId);
            }
        }
    }

    // Invia notifica push a un utente
    async sendPushNotification(userId, title, body, data = {}) {
        try {
            const subscriptions = this.subscriptions.get(userId);
            if (!subscriptions || subscriptions.length === 0) {
                console.log(`⚠️ Nessun dispositivo registrato per utente ${userId}`);
                return;
            }

            // Qui si integra con Firebase Cloud Messaging o altri servizi
            // Per ora simuliamo l'invio
            subscriptions.forEach((sub, index) => {
                console.log(`📱 Push inviata a dispositivo ${index + 1}:`, { title, body, data });
            });

            return {
                success: true,
                sent: subscriptions.length
            };
        } catch (error) {
            console.error('❌ Errore invio push:', error);
            throw error;
        }
    }

    // Notifica di nuovo messaggio
    async notifyNewMessage(userId, sender, message) {
        return this.sendPushNotification(
            userId,
            `💬 Nuovo messaggio da ${sender}`,
            message,
            { type: 'message', sender }
        );
    }

    // Notifica di nuovo pagamento
    async notifyPayment(userId, amount, currency) {
        return this.sendPushNotification(
            userId,
            '💰 Nuovo pagamento ricevuto!',
            `Hai ricevuto ${amount} ${currency}`,
            { type: 'payment', amount, currency }
        );
    }

    // Notifica di bounty
    async notifyBounty(userId, bountyTitle, status) {
        return this.sendPushNotification(
            userId,
            `🎯 Bounty ${status}`,
            `Il bounty "${bountyTitle}" è stato ${status === 'completed' ? 'completato' : 'assegnato'}`,
            { type: 'bounty', status }
        );
    }

    // Notifica di pianta registrata
    async notifyPlantRegistered(userId, plantName) {
        return this.sendPushNotification(
            userId,
            '🌿 Nuova pianta registrata!',
            `Hai registrato "${plantName}" nel database`,
            { type: 'plant', plantName }
        );
    }
}

module.exports = { PushManager };
