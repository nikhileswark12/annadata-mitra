const express = require('express');
const router = express.Router();
const marketController = require('../controllers/marketController');
const { validateMarketInsights } = require('../middleware/validate');
const authMiddleware = require('../middleware/authMiddleware');

// Get market insights
router.post('/insights', authMiddleware, validateMarketInsights, marketController.getInsights);

// Get market history
router.get('/history', authMiddleware, marketController.history);

module.exports = router;