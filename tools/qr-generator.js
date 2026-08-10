#!/usr/bin/env node
const QRCode = require('qrcode');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('🟣 Generatore QR Code per pagamenti XMR\n');

rl.question('📤 Inserisci indirizzo XMR: ', (address) => {
  if (!address || address.length < 10) {
    console.log('❌ Indirizzo non valido.');
    rl.close();
    return;
  }

  rl.question('💰 Inserisci importo (in XMR, opzionale): ', (amount) => {
    let uri = `monero:${address}`;
    if (amount && parseFloat(amount) > 0) {
      uri += `?amount=${parseFloat(amount)}`;
    }

    const filename = `xmr-qr-${Date.now()}.png`;
    QRCode.toFile(filename, uri, { width: 400 }, (err) => {
      if (err) {
        console.error('❌ Errore generazione QR:', err);
      } else {
        console.log(`✅ QR Code salvato: ${filename}`);
        console.log(`🔗 URI: ${uri}`);
      }
      rl.close();
    });
  });
});
