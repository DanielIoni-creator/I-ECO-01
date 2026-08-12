/**
 * 🌐 Social Controller - Gestione Social
 */

const { SocialService } = require('../services/social.service');

class SocialController {
    constructor() {
        this.socialService = new SocialService();
    }

    // Ottieni stato piattaforme
    async getStatus(req, res) {
        try {
            const status = this.socialService.getPlatformsStatus();
            res.json({
                success: true,
                data: status
            });
        } catch (error) {
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Condividi su Twitter
    async shareTwitter(req, res) {
        try {
            const { content } = req.body;
            const result = await this.socialService.shareOnTwitter(content);
            res.json(result);
        } catch (error) {
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Invia Telegram
    async sendTelegram(req, res) {
        try {
            const { message } = req.body;
            const result = await this.socialService.sendTelegramMessage(message);
            res.json(result);
        } catch (error) {
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Invia Discord
    async sendDiscord(req, res) {
        try {
            const { message } = req.body;
            const result = await this.socialService.sendDiscordMessage(message);
            res.json(result);
        } catch (error) {
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Condividi pianta
    async sharePlant(req, res) {
        try {
            const { plantData } = req.body;
            const result = await this.socialService.shareNewPlant(plantData);
            res.json(result);
        } catch (error) {
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Condividi bounty
    async shareBounty(req, res) {
        try {
            const { bountyData } = req.body;
            const result = await this.socialService.shareNewBounty(bountyData);
            res.json(result);
        } catch (error) {
            res.status(500).json({ success: false, error: error.message });
        }
    }

    // Condividi pagamento
    async sharePayment(req, res) {
        try {
            const { paymentData } = req.body;
            const result = await this.socialService.sharePayment(paymentData);
            res.json(result);
        } catch (error) {
            res.status(500).json({ success: false, error: error.message });
        }
    }
}

module.exports = { SocialController };
