/**
 * 📡 NFC Routes
 */

const express = require('express');
const router = express.Router();
const { NFCController } = require('./nfc.controller');

const nfcController = new NFCController();

// Route pubbliche
router.post('/scan', (req, res) => nfcController.scanTag(req, res));
router.post('/verify', (req, res) => nfcController.verifyTag(req, res));
router.get('/status', (req, res) => nfcController.getStatus(req, res));
router.post('/register', (req, res) => nfcController.registerTag(req, res));

module.exports = router;
