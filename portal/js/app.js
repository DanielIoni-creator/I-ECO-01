// ============================================
// PYTHO PORTAL - Main Application
// ============================================

// Stato globale
const state = {
    isLoggedIn: false,
    user: null,
    users: JSON.parse(localStorage.getItem('myzubster_users') || '[]'),
    chatHistory: [],
    sensors: {
        temperature: 22.5,
        humidity: 65,
        soil: 45,
        light: 800
    }
};

// ============================================
// AUTH FUNCTIONS
// ============================================

function toggleLogin() {
    const modal = document.getElementById('authModal');
    if (modal.style.display === 'flex') {
        modal.style.display = 'none';
    } else {
        modal.style.display = 'flex';
    }
}

function switchAuth(form) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const title = document.getElementById('authTitle');
    
    if (form === 'login') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        title.textContent = '🔐 Accedi a MyZubster';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        title.textContent = '🪙 Registrati a MyZubster';
    }
}

// Registrazione
document.getElementById('registerForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('regName').value;
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const passwordConfirm = document.getElementById('regPasswordConfirm').value;
    const comune = document.getElementById('regComune').value;
    
    if (password !== passwordConfirm) {
        alert('❌ Le password non coincidono!');
        return;
    }
    
    if (password.length < 6) {
        alert('❌ La password deve avere almeno 6 caratteri!');
        return;
    }
    
    if (!comune) {
        alert('❌ Seleziona un comune!');
        return;
    }
    
    if (state.users.find(u => u.email === email)) {
        alert('❌ Questa email è già registrata!');
        return;
    }
    
    const newUser = {
        id: 'user_' + Date.now(),
        name: name,
        email: email,
        password: password,
        comune: comune,
        wallets: { myz: 0, xmr: 0 },
        registered_at: new Date().toISOString()
    };
    
    state.users.push(newUser);
    localStorage.setItem('myzubster_users', JSON.stringify(state.users));
    
    alert('✅ Registrazione completata! Ora puoi accedere.');
    switchAuth('login');
    document.getElementById('loginEmail').value = email;
});

// Login
document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    const user = state.users.find(u => u.email === email && u.password === password);
    
    if (!user) {
        alert('❌ Email o password errati!');
        return;
    }
    
    state.isLoggedIn = true;
    state.user = user;
    toggleLogin();
    updateUserProfile();
    document.getElementById('userCount').textContent = state.users.length;
    
    askPytho(`👋 Benvenuto ${user.name}! Sei registrato a ${user.comune}`);
});

function logout() {
    state.isLoggedIn = false;
    state.user = null;
    document.getElementById('userProfile').style.display = 'none';
    document.getElementById('loginBtn').textContent = '🔐 Accedi';
    askPytho('👋 Arrivederci! Tornerai?');
}

function updateUserProfile() {
    if (!state.user) return;
    
    const profile = document.getElementById('userProfile');
    profile.style.display = 'block';
    
    document.getElementById('userName').textContent = state.user.name;
    document.getElementById('userEmail').textContent = state.user.email;
    document.getElementById('userMyzWallet').textContent = state.user.wallets.myz.toFixed(2) + ' MYZ';
    document.getElementById('userXmrWallet').textContent = state.user.wallets.xmr.toFixed(2) + ' XMR';
    document.getElementById('registeredComune').textContent = state.user.comune;
    document.getElementById('loginBtn').textContent = '👤 ' + state.user.name;
}

function registerComune() {
    if (!state.user) {
        alert('❌ Devi essere registrato per registrare un comune!');
        toggleLogin();
        return;
    }
    
    const comune = prompt('Inserisci il nome del comune da registrare:', state.user.comune || '');
    if (comune && comune.trim()) {
        state.user.comune = comune.trim();
        const index = state.users.findIndex(u => u.id === state.user.id);
        if (index !== -1) {
            state.users[index] = state.user;
            localStorage.setItem('myzubster_users', JSON.stringify(state.users));
        }
        document.getElementById('registeredComune').textContent = state.user.comune;
        askPytho(`🏛️ Comune ${state.user.comune} registrato con successo!`);
    }
}

// ============================================
// CHAT FUNCTIONS
// ============================================

async function askPytho(message) {
    const input = document.getElementById('chatInput');
    const messages = document.getElementById('chatMessages');
    
    if (!message && input) {
        message = input.value.trim();
        if (!message) return;
        input.value = '';
    }
    
    addMessage('user', message);
    
    try {
        const response = await fetch('/api/pytho/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        addMessage('pytho', data.response || data.pytho_says || '👽 Pytho sta pensando...');
    } catch (error) {
        addMessage('pytho', '👽 Mi dispiace, ho avuto un problema. Riprova più tardi.');
    }
}

function addMessage(type, text) {
    const messages = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = `message ${type}`;
    
    const avatar = type === 'pytho' ? '👽' : '🧑';
    const name = type === 'pytho' ? 'Pytho' : 'Tu';
    
    div.innerHTML = `
        <span class="avatar">${avatar}</span>
        <div class="message-content">
            <strong>${name}</strong>
            <p>${text}</p>
        </div>
    `;
    
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

// ============================================
// SENSOR FUNCTIONS
// ============================================

function updateSensors() {
    state.sensors.temperature = (20 + Math.random() * 5).toFixed(1);
    state.sensors.humidity = Math.floor(60 + Math.random() * 20);
    state.sensors.soil = Math.floor(30 + Math.random() * 40);
    state.sensors.light = Math.floor(500 + Math.random() * 500);
    
    document.getElementById('tempValue').textContent = `${state.sensors.temperature}°C`;
    document.getElementById('humidityValue').textContent = `${state.sensors.humidity}%`;
    document.getElementById('soilValue').textContent = `${state.sensors.soil}%`;
    document.getElementById('lightValue').textContent = `${state.sensors.light} lux`;
}

// ============================================
// COMMAND FUNCTIONS
// ============================================

function sendCommand(command) {
    console.log('📡 Comando inviato:', command);
    askPytho(`Esegui comando: ${command}`);
    
    const btn = document.querySelector(`[onclick*="${command}"]`);
    if (btn) {
        btn.style.background = 'rgba(34, 197, 94, 0.3)';
        setTimeout(() => {
            btn.style.background = '';
        }, 500);
    }
}

// ============================================
// PAYMENT FUNCTIONS
// ============================================

async function createPayment() {
    if (!state.user) {
        alert('❌ Devi essere registrato per creare un pagamento!');
        toggleLogin();
        return;
    }
    
    try {
        const amount = Math.floor(Math.random() * 10) + 1;
        const response = await fetch('/api/myz/payment/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tag_id: `PORTAL-${Date.now()}`,
                amount: amount
            })
        });
        const data = await response.json();
        if (data.success) {
            state.user.wallets.myz += amount;
            const index = state.users.findIndex(u => u.id === state.user.id);
            if (index !== -1) {
                state.users[index] = state.user;
                localStorage.setItem('myzubster_users', JSON.stringify(state.users));
            }
            updateUserProfile();
            askPytho(`💰 Pagamento creato! +${amount} MYZ`);
        }
    } catch (error) {
        console.error('Errore pagamento:', error);
    }
}

async function updatePayments() {
    try {
        const response = await fetch('/api/myz/stats');
        const data = await response.json();
        if (data.success) {
            document.getElementById('myzBalance').textContent = `${data.stats.total_amount || 0} MYZ`;
        }
    } catch (error) {
        console.error('Errore aggiornamento pagamenti:', error);
    }
}

// ============================================
// DASHBOARD FUNCTIONS
// ============================================

async function updateDashboard() {
    try {
        const response = await fetch('/api/dashboard');
        const data = await response.json();
        if (data.success) {
            document.getElementById('totalPayments').textContent = data.dashboard.total_payments || 0;
            document.getElementById('plantCount').textContent = data.dashboard.total_payments || 24;
        }
    } catch (error) {
        console.error('Errore dashboard:', error);
    }
}

// ============================================
// CHART FUNCTIONS
// ============================================

function drawChart() {
    const canvas = document.getElementById('chartCanvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.parentElement.clientWidth - 24;
    const height = 100;
    
    canvas.width = width;
    canvas.height = height;
    
    ctx.clearRect(0, 0, width, height);
    
    ctx.strokeStyle = 'rgba(255,255,255,0.1)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, height/2);
    ctx.lineTo(width, height/2);
    ctx.stroke();
    
    const data = Array.from({length: 20}, () => Math.random() * 60 + 20);
    const step = width / data.length;
    
    ctx.strokeStyle = '#a855f7';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    data.forEach((value, i) => {
        const x = i * step;
        const y = height - (value / 100 * height);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();
    
    ctx.fillStyle = 'rgba(168, 85, 247, 0.1)';
    ctx.beginPath();
    ctx.moveTo(0, height);
    data.forEach((value, i) => {
        const x = i * step;
        const y = height - (value / 100 * height);
        ctx.lineTo(x, y);
    });
    ctx.lineTo(width, height);
    ctx.closePath();
    ctx.fill();
}

// ============================================
// EVENT LISTENERS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('chatInput');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askPytho();
            }
        });
    }
    
    const sendBtn = document.getElementById('chatSend');
    if (sendBtn) {
        sendBtn.addEventListener('click', function() {
            askPytho();
        });
    }
    
    document.getElementById('userCount').textContent = state.users.length;
    
    updateSensors();
    updatePayments();
    updateDashboard();
    
    setInterval(updateSensors, 5000);
    setInterval(updatePayments, 30000);
    setInterval(updateDashboard, 30000);
    
    setTimeout(drawChart, 500);
    window.addEventListener('resize', drawChart);
});

// ============================================
// EXPOSE FUNCTIONS GLOBALLY
// ============================================

window.askPytho = askPytho;
window.sendCommand = sendCommand;
window.createPayment = createPayment;
window.registerComune = registerComune;
window.toggleLogin = toggleLogin;
window.switchAuth = switchAuth;
window.logout = logout;

// ============================================
// 👛 FUNZIONI WALLET
// ============================================

// Ottieni il wallet dell'utente
async function getWallet(userId) {
    try {
        const response = await fetch(`/api/wallet/${userId}`);
        const data = await response.json();
        
        if (data.success) {
            updateWalletUI(data.wallet);
            return data.wallet;
        }
        return null;
    } catch (error) {
        console.error('❌ Errore recupero wallet:', error);
        return null;
    }
}

// Aggiorna UI del wallet
function updateWalletUI(wallet) {
    if (wallet) {
        document.getElementById('myzBalance').textContent = `${wallet.myz.balance.toFixed(2)} MYZ`;
        document.getElementById('xmrBalance').textContent = `${wallet.xmr.balance.toFixed(4)} XMR`;
        
        // Salva nel localStorage
        localStorage.setItem('myzBalance', wallet.myz.balance);
        localStorage.setItem('xmrBalance', wallet.xmr.balance);
    }
}

// Crea un pagamento MYZ
async function createPayment(amount, description = 'Pagamento MYZ') {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        alert('❌ Devi essere loggato per creare un pagamento');
        return;
    }
    
    try {
        const response = await fetch('/api/payment/myz/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: userId,
                amount: amount || 10,
                description: description
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`✅ Pagamento MYZ creato con successo!\nImporto: ${data.payment.amount} MYZ\nIndirizzo: ${data.payment.address}`);
            return data.payment;
        } else {
            alert(`❌ Errore: ${data.error}`);
        }
    } catch (error) {
        console.error('❌ Errore creazione pagamento:', error);
        alert('❌ Errore durante la creazione del pagamento');
    }
}

// Crea un pagamento XMR
async function createXMRPayment(amount, description = 'Pagamento XMR') {
    const userId = localStorage.getItem('userId');
    if (!userId) {
        alert('❌ Devi essere loggato per creare un pagamento');
        return;
    }
    
    try {
        const response = await fetch('/api/payment/xmr/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                userId: userId,
                amount: amount || 0.01,
                description: description
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`✅ Pagamento XMR creato con successo!\nImporto: ${data.payment.amount} XMR\nIndirizzo: ${data.payment.address}`);
            return data.payment;
        } else {
            alert(`❌ Errore: ${data.error}`);
        }
    } catch (error) {
        console.error('❌ Errore creazione pagamento XMR:', error);
        alert('❌ Errore durante la creazione del pagamento XMR');
    }
}

// Aggiorna il saldo del wallet
async function updateBalance(userId) {
    const wallet = await getWallet(userId);
    if (wallet) {
        updateWalletUI(wallet);
    }
}

// Carica i pagamenti dell'utente
async function loadPayments(userId) {
    try {
        const response = await fetch(`/api/payments/${userId}`);
        const data = await response.json();
        
        if (data.success) {
            const paymentsList = document.getElementById('paymentsList');
            if (paymentsList) {
                paymentsList.innerHTML = data.payments.map(p => `
                    <div class="payment-item ${p.status}">
                        <span>${p.description}</span>
                        <span>${p.amount} ${p.currency}</span>
                        <span class="payment-status">${p.status}</span>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        console.error('❌ Errore caricamento pagamenti:', error);
    }
}
