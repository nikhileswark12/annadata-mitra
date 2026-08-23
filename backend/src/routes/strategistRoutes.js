const express = require('express');
const router = express.Router();
const strategistController = require('../controllers/strategistController');
const { validateStrategy } = require('../middleware/validate');
const authMiddleware = require('../middleware/authMiddleware');

// Generate strategy
router.post('/generate', authMiddleware, validateStrategy, strategistController.generate);

// Get strategy history
router.get('/history', authMiddleware, strategistController.history);

module.exports = router;
