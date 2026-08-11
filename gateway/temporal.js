document.addEventListener('DOMContentLoaded', () => { loadTimeline(); loadFlux(); });

async function travel() {
    const dest = document.getElementById('dest').value;
    const year = document.getElementById('year').value;
    const result = document.getElementById('result');
    result.style.display = 'block';
    result.innerHTML = '🛸 Viaggio in corso...';
    
    try {
        const r = await fetch('/api/pytho/timetravel', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ destination: dest, year })
        });
        const data = await r.json();
        result.innerHTML = `✅ Viaggio completato!<br>🛸 ${data.travel.destination}<br>📅 ${data.travel.year}<br>${data.travel.pytho}`;
        loadTimeline();
    } catch(e) {
        result.innerHTML = '❌ Errore: ' + e.message;
    }
}

async function loadTimeline() {
    try {
        const r = await fetch('/api/pytho/timeline');
        const data = await r.json();
        let html = '';
        data.timeline.forEach(e => {
            html += `<div class="timeline-item"><span class="year">${e.year}</span><span>${e.event}</span><span>${e.status}</span></div>`;
        });
        document.getElementById('timeline').innerHTML = html;
    } catch(e) {}
}

async function loadFlux() {
    try {
        const r = await fetch('/api/pytho/flux');
        const data = await r.json();
        document.getElementById('flux').textContent = data.flux.power;
        document.getElementById('status').textContent = data.flux.status;
        document.getElementById('charge').textContent = data.flux.charge;
    } catch(e) {}
}
setInterval(loadFlux, 3000);
