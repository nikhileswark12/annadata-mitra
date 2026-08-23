const express = require('express');
const router = express.Router();
const visionController = require('../controllers/visionController');
const authMiddleware = require('../middleware/authMiddleware');

// Analyze image for disease
router.post('/analyze', authMiddleware, visionController.upload.single('image'), visionController.analyze);

// Get disease detection history
router.get('/history', authMiddleware, visionController.history);

module.exports = router;