const express = require('express');
const router = express.Router();

const payments = {};

// Crea pagamento
router.post('/payment/create', (req, res) => {
  const { tag_id, amount = 0.01 } = req.body;
  const address = '45M4DW1ug8bdQowWpxucTpgsfjLbVxbYaAra79VewmBobuuhgqTjyD4R3DzpqLM2veiphcB16n24qN1QbLg3y2PYGK3Qkoe';
  const payment_id = 'pay_' + Date.now();

  payments[payment_id] = { tag_id, amount, address, status: 'pending' };

  res.json({
    success: true,
    payment_id,
    address,
    amount,
    qr_code: `monero:${address}?amount=${amount}`,
    tag: tag_id
  });
});

// Verifica stato
router.get('/payment/status/:id', (req, res) => {
  const payment = payments[req.params.id];
  if (!payment) {
    return res.status(404).json({ success: false, error: 'Pagamento non trovato' });
  }
  res.json({ success: true, payment_id: req.params.id, status: payment.status });
});

// Lista pagamenti
router.get('/payments', (req, res) => {
  const list = Object.keys(payments).map(id => ({ id, ...payments[id] }));
  res.json({ success: true, count: list.length, payments: list });
});

module.exports = router;
