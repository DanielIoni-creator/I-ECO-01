/**
 * 📧 Email Service - Gestione Email
 */

const nodemailer = require('nodemailer');

class EmailService {
    constructor() {
        this.transporter = nodemailer.createTransport({
            host: process.env.SMTP_HOST || 'smtp.gmail.com',
            port: process.env.SMTP_PORT || 587,
            secure: false,
            auth: {
                user: process.env.SMTP_USER || 'myzubster@gmail.com',
                pass: process.env.SMTP_PASS || 'password'
            }
        });
    }

    // Template base
    getBaseTemplate(content, title = 'MyZubster') {
        return `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; background: #0f0c29; color: #fff; padding: 20px; }
                    .container { max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; }
                    .header { text-align: center; margin-bottom: 30px; }
                    .header h1 { color: #8b5cf6; }
                    .content { line-height: 1.6; }
                    .footer { text-align: center; margin-top: 30px; color: #888; font-size: 12px; }
                    .button { display: inline-block; padding: 12px 24px; background: #8b5cf6; color: #fff; text-decoration: none; border-radius: 8px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>👽 MyZubster</h1>
                        <h2>${title}</h2>
                    </div>
                    <div class="content">
                        ${content}
                    </div>
                    <div class="footer">
                        <p>© 2026 MyZubster. Tutti i diritti riservati.</p>
                        <p>👽 Pytho ti saluta!</p>
                    </div>
                </div>
            </body>
            </html>
        `;
    }

    // Invia email
    async sendEmail(to, subject, content, html = true) {
        try {
            const mailOptions = {
                from: 'MyZubster <myzubster@gmail.com>',
                to,
                subject,
                html: html ? this.getBaseTemplate(content, subject) : content
            };

            const info = await this.transporter.sendMail(mailOptions);
            console.log('✅ Email inviata:', info.messageId);
            return info;
        } catch (error) {
            console.error('❌ Errore invio email:', error);
            throw error;
        }
    }

    // Notifica di benvenuto
    async sendWelcomeEmail(email, name) {
        const content = `
            <p>Ciao <strong>${name}</strong>! 👋</p>
            <p>Benvenuto in <strong>MyZubster</strong>! Siamo felici di averti con noi.</p>
            <p>Con MyZubster puoi:</p>
            <ul>
                <li>🌿 Registrare piante e animali</li>
                <li>💰 Effettuare pagamenti in XMR e MYZ</li>
                <li>👽 Chiacchierare con Pytho</li>
                <li>🛸 Viaggiare nel tempo</li>
            </ul>
            <p>Inizia subito la tua avventura!</p>
            <p style="text-align: center;">
                <a href="https://myzubster.com" class="button">Vai al portale</a>
            </p>
        `;
        return this.sendEmail(email, '👽 Benvenuto in MyZubster!', content);
    }

    // Notifica di pagamento ricevuto
    async sendPaymentNotification(email, amount, currency, txId) {
        const content = `
            <p>Ciao! 👋</p>
            <p>Hai ricevuto un pagamento di <strong>${amount} ${currency}</strong>!</p>
            <p>ID Transazione: <code>${txId}</code></p>
            <p>Il pagamento è stato confermato e il saldo è stato aggiornato.</p>
            <p style="text-align: center;">
                <a href="https://myzubster.com/dashboard" class="button">Vedi dashboard</a>
            </p>
        `;
        return this.sendEmail(email, '💰 Pagamento Ricevuto!', content);
    }

    // Notifica di bounty completato
    async sendBountyNotification(email, bountyTitle, reward) {
        const content = `
            <p>Complimenti! 🎉</p>
            <p>Hai completato il bounty: <strong>${bountyTitle}</strong></p>
            <p>Ricompensa: <strong>${reward} MYZ</strong></p>
            <p>Il tuo saldo è stato aggiornato automaticamente.</p>
            <p style="text-align: center;">
                <a href="https://myzubster.com/bounties" class="button">Vedi bounty</a>
            </p>
        `;
        return this.sendEmail(email, '🎯 Bounty Completato!', content);
    }

    // Reset password
    async sendResetPasswordEmail(email, resetToken) {
        const resetLink = `https://myzubster.com/reset-password?token=${resetToken}`;
        const content = `
            <p>Ciao! 👋</p>
            <p>Hai richiesto il reset della password.</p>
            <p>Clicca sul link qui sotto per reimpostare la tua password:</p>
            <p style="text-align: center;">
                <a href="${resetLink}" class="button">Reimposta password</a>
            </p>
            <p>Il link è valido per 24 ore.</p>
            <p>Se non hai richiesto tu questo reset, ignora questa email.</p>
        `;
        return this.sendEmail(email, '🔐 Reset Password MyZubster', content);
    }
}

module.exports = { EmailService };
