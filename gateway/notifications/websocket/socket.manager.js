/**
 * 🔔 Socket Manager - Gestione WebSocket
 */

const { Server } = require('socket.io');
const jwt = require('jsonwebtoken');

class SocketManager {
    constructor(server) {
        this.io = new Server(server, {
            cors: {
                origin: '*',
                methods: ['GET', 'POST']
            }
        });
        
        this.clients = new Map();
        this.setupMiddleware();
        this.setupEvents();
    }

    // Setup middleware per autenticazione
    setupMiddleware() {
        this.io.use((socket, next) => {
            const token = socket.handshake.auth.token;
            if (!token) {
                return next(new Error('Token non fornito'));
            }

            try {
                const decoded = jwt.verify(token, process.env.JWT_SECRET || 'myzubster_secret_key_2026');
                socket.userId = decoded.id;
                socket.userRole = decoded.role;
                next();
            } catch (error) {
                next(new Error('Token non valido'));
            }
        });
    }

    // Setup eventi Socket.IO
    setupEvents() {
        this.io.on('connection', (socket) => {
            console.log(`🔌 Client connesso: ${socket.id} (User: ${socket.userId})`);
            
            // Salva il client
            if (socket.userId) {
                if (!this.clients.has(socket.userId)) {
                    this.clients.set(socket.userId, []);
                }
                this.clients.get(socket.userId).push(socket);
            }

            // Evento per unirsi a una room
            socket.on('join-room', (room) => {
                socket.join(room);
                console.log(`📢 Client ${socket.id} si è unito alla room: ${room}`);
            });

            // Evento per lasciare una room
            socket.on('leave-room', (room) => {
                socket.leave(room);
                console.log(`📢 Client ${socket.id} ha lasciato la room: ${room}`);
            });

            // Evento per notifiche
            socket.on('notification', (data) => {
                console.log(`📨 Notifica da ${socket.id}:`, data);
                // Invia a tutti nella room
                this.io.to(data.room || 'general').emit('notification', data);
            });

            // Disconnessione
            socket.on('disconnect', () => {
                console.log(`🔌 Client disconnesso: ${socket.id}`);
                if (socket.userId && this.clients.has(socket.userId)) {
                    const clients = this.clients.get(socket.userId);
                    const index = clients.indexOf(socket);
                    if (index > -1) {
                        clients.splice(index, 1);
                    }
                    if (clients.length === 0) {
                        this.clients.delete(socket.userId);
                    }
                }
            });
        });
    }

    // Invia notifica a un utente specifico
    sendToUser(userId, event, data) {
        const clients = this.clients.get(userId);
        if (clients) {
            clients.forEach(client => {
                client.emit(event, data);
            });
            return true;
        }
        return false;
    }

    // Invia notifica a una room
    sendToRoom(room, event, data) {
        this.io.to(room).emit(event, data);
    }

    // Invia notifica a tutti
    broadcast(event, data) {
        this.io.emit(event, data);
    }

    // Notifica di pagamento ricevuto
    notifyPayment(userId, paymentData) {
        this.sendToUser(userId, 'payment-received', {
            type: 'payment',
            data: paymentData,
            timestamp: new Date().toISOString()
        });
    }

    // Notifica di bounty completato
    notifyBountyCompleted(userId, bountyData) {
        this.sendToUser(userId, 'bounty-completed', {
            type: 'bounty',
            data: bountyData,
            timestamp: new Date().toISOString()
        });
    }

    // Notifica di nuova pianta registrata
    notifyNewPlant(plantData) {
        this.broadcast('new-plant', {
            type: 'plant',
            data: plantData,
            timestamp: new Date().toISOString()
        });
    }
}

module.exports = { SocketManager };
