/**
 * 🙏 Orti Francescani Routes
 */

const express = require('express');
const router = express.Router();
const { OrtiFrancescaniController } = require('../controllers/orto.controller');

const controller = new OrtiFrancescaniController();

// Route pubbliche (tutte)
router.post('/register', (req, res) => controller.registerOrto(req, res));
router.get('/', (req, res) => controller.getOrti(req, res));
router.get('/stats', (req, res) => controller.getStats(req, res));
router.get('/:id', (req, res) => controller.getOrto(req, res));
router.post('/:id/plants', (req, res) => controller.addPlant(req, res));

module.exports = router;
