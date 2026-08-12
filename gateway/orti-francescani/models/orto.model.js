/**
 * 🙏 Orto Francescano Model
 */

class OrtoFrancescano {
    constructor(data) {
        this.id = data.id || `orto_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
        this.nome = data.nome;
        this.parrocchia = data.parrocchia;
        this.indirizzo = data.indirizzo;
        this.citta = data.citta || 'Rimini';
        this.coordinate = data.coordinate || { lat: 0, lng: 0 };
        this.contatto = data.contatto || {
            nome: '',
            telefono: '',
            email: ''
        };
        this.stato = data.stato || 'attivo'; // attivo, inattivo, in_attesa
        this.piante = data.piante || [];
        this.volontari = data.volontari || [];
        this.donazioni = data.donazioni || [];
        this.stats = {
            totale_piante: 0,
            totale_volontari: 0,
            totale_donazioni: 0,
            totale_myz_distribuiti: 0
        };
        this.createdAt = data.createdAt || new Date().toISOString();
        this.updatedAt = data.updatedAt || new Date().toISOString();
    }

    // Aggiungi pianta
    addPlant(plantData) {
        const plant = {
            id: `plant_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
            ...plantData,
            registratoDa: plantData.volontarioId || 'sconosciuto',
            timestamp: new Date().toISOString()
        };
        this.piante.push(plant);
        this.stats.totale_piante = this.piante.length;
        this.updatedAt = new Date().toISOString();
        return plant;
    }

    // Aggiungi volontario
    addVolunteer(volunteerData) {
        const volunteer = {
            id: `vol_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
            ...volunteerData,
            pianteMappate: 0,
            myzGuadagnati: 0,
            joinedAt: new Date().toISOString()
        };
        this.volontari.push(volunteer);
        this.stats.totale_volontari = this.volontari.length;
        this.updatedAt = new Date().toISOString();
        return volunteer;
    }

    // Aggiungi donazione
    addDonation(donationData) {
        const donation = {
            id: `don_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`,
            ...donationData,
            timestamp: new Date().toISOString()
        };
        this.donazioni.push(donation);
        this.stats.totale_donazioni += donation.amount || 0;
        this.updatedAt = new Date().toISOString();
        return donation;
    }

    toJSON() {
        return {
            id: this.id,
            nome: this.nome,
            parrocchia: this.parrocchia,
            indirizzo: this.indirizzo,
            citta: this.citta,
            coordinate: this.coordinate,
            contatto: this.contatto,
            stato: this.stato,
            piante: this.piante.slice(-10),
            volontari: this.volontari.slice(-10),
            stats: this.stats,
            createdAt: this.createdAt,
            updatedAt: this.updatedAt
        };
    }
}

module.exports = { OrtoFrancescano };
