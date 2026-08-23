const express = require('express');
const router = express.Router();
const weatherController = require('../controllers/weatherController');
const { validateWeatherRisk } = require('../middleware/validate');
const authMiddleware = require('../middleware/authMiddleware');

// Get weather risks
router.post('/risk', authMiddleware, validateWeatherRisk, weatherController.getRisk);

// Get weather risk history
router.get('/history', authMiddleware, weatherController.history);

module.exports = router;