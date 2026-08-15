const crypto = require('crypto');

class EscrowController {
    constructor() {
        this.escrows = new Map();
        this.threshold = process.env.ESCROW_MULTISIG_THRESHOLD || 2;
        this.signers = process.env.ESCROW_MULTISIG_SIGNERS || 3;
        this.timeoutHours = parseInt(process.env.ESCROW_TIMEOUT_HOURS) || 24;
        this.feePercent = parseFloat(process.env.ESCROW_FEE_PERCENT) || 0.5;
        this.treasuryAddress = process.env.TREASURY_ADDRESS;
        this.adminWallet = process.env.ADMIN_WALLET;

        console.log('🔐 Escrow Controller inizializzato');
        console.log(`   Threshold: ${this.threshold}/${this.signers}`);
        console.log(`   Timeout: ${this.timeoutHours}h`);
        console.log(`   Fee: ${this.feePercent}%`);
    }

    async createEscrow(data) {
        const { serviceId, buyerAddress, sellerAddress, amount, description, metadata = {} } = data;
        if (!serviceId) throw new Error('serviceId è richiesto');
        if (!buyerAddress) throw new Error('buyerAddress è richiesto');
        if (!sellerAddress) throw new Error('sellerAddress è richiesto');
        if (!amount || amount <= 0) throw new Error('amount deve essere positivo');

        const escrowId = `ESC-${Date.now()}-${crypto.randomBytes(4).toString('hex').toUpperCase()}`;
        const now = new Date();
        const expiresAt = new Date(now.getTime() + this.timeoutHours * 3600000);

        const escrow = {
            escrowId,
            serviceId,
            buyerAddress,
            sellerAddress,
            amount,
            description,
            metadata,
            status: 'PENDING',
            createdAt: now.toISOString(),
            expiresAt: expiresAt.toISOString(),
            signatures: [],
            releaseHash: null,
            txHash: null,
            fee: amount * (this.feePercent / 100),
            releaseAmount: amount * (1 - this.feePercent / 100)
        };

        this.escrows.set(escrowId, escrow);
        console.log(`📝 Escrow creato: ${escrowId}`);
        console.log(`   Service: ${serviceId}`);
        console.log(`   Amount: ${amount} XMR`);
        console.log(`   Fee: ${escrow.fee} XMR`);
        console.log(`   Net: ${escrow.releaseAmount} XMR`);

        return escrow;
    }

    async signEscrow(escrowId, signerAddress, signature) {
        const escrow = this.escrows.get(escrowId);
        if (!escrow) throw new Error(`Escrow ${escrowId} non trovato`);
        if (escrow.status !== 'PENDING') throw new Error(`Escrow ${escrowId} non è in stato PENDING`);
        if (escrow.signatures.some(s => s.signer === signerAddress)) {
            throw new Error(`Firmatario ha già firmato`);
        }

        escrow.signatures.push({
            signer: signerAddress,
            signature,
            timestamp: new Date().toISOString()
        });

        console.log(`📝 Firma aggiunta per escrow ${escrowId}`);
        console.log(`   Firme: ${escrow.signatures.length}/${this.threshold}`);

        if (escrow.signatures.length >= this.threshold) {
            escrow.status = 'SIGNED';
            escrow.releaseHash = crypto.createHash('sha256')
                .update(`${escrow.escrowId}:${escrow.sellerAddress}:${escrow.amount}`)
                .digest('hex');
            console.log(`✅ Escrow ${escrowId} ha raggiunto la soglia!`);
        }

        return escrow;
    }

    async releaseEscrow(escrowId, releaseSignature) {
        const escrow = this.escrows.get(escrowId);
        if (!escrow) throw new Error(`Escrow ${escrowId} non trovato`);
        if (escrow.status !== 'SIGNED') throw new Error(`Escrow ${escrowId} non è firmato`);

        escrow.status = 'RELEASED';
        escrow.releasedAt = new Date().toISOString();
        escrow.releaseSignature = releaseSignature;

        console.log(`💰 Escrow ${escrowId} rilasciato!`);
        console.log(`   Amount: ${escrow.releaseAmount} XMR`);
        console.log(`   Fee: ${escrow.fee} XMR`);

        return escrow;
    }

    async cancelEscrow(escrowId, reason = 'Cancellato dall\'utente') {
        const escrow = this.escrows.get(escrowId);
        if (!escrow) throw new Error(`Escrow ${escrowId} non trovato`);
        if (escrow.status === 'RELEASED') throw new Error(`Escrow ${escrowId} è già stato rilasciato`);

        escrow.status = 'CANCELLED';
        escrow.cancelledAt = new Date().toISOString();
        escrow.cancelReason = reason;

        console.log(`❌ Escrow ${escrowId} cancellato`);
        return escrow;
    }

    getEscrowStatus(escrowId) {
        const escrow = this.escrows.get(escrowId);
        if (!escrow) return { error: 'Escrow non trovato' };
        return {
            escrowId: escrow.escrowId,
            serviceId: escrow.serviceId,
            status: escrow.status,
            amount: escrow.amount,
            releaseAmount: escrow.releaseAmount,
            fee: escrow.fee,
            signatures: escrow.signatures.length,
            requiredSignatures: this.threshold,
            createdAt: escrow.createdAt,
            expiresAt: escrow.expiresAt,
            ...(escrow.releasedAt && { releasedAt: escrow.releasedAt }),
            ...(escrow.cancelledAt && { cancelledAt: escrow.cancelledAt })
        };
    }

    listEscrows(filters = {}) {
        let results = Array.from(this.escrows.values());
        if (filters.status) results = results.filter(e => e.status === filters.status);
        if (filters.buyerAddress) results = results.filter(e => e.buyerAddress === filters.buyerAddress);
        if (filters.sellerAddress) results = results.filter(e => e.sellerAddress === filters.sellerAddress);
        return results;
    }
}

module.exports = EscrowController;
