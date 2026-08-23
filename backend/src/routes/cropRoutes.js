const express = require('express');
const router = express.Router();
const cropController = require('../controllers/cropController');
const { validateCropRecommend } = require('../middleware/validate');
const authMiddleware = require('../middleware/authMiddleware');

// Recommend crops based on soil and weather
router.post('/recommend', authMiddleware, validateCropRecommend, cropController.recommend);

// Get crop planning history
router.get('/history', authMiddleware, cropController.history);

module.exports = router;