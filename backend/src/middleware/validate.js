const { body, validationResult } = require('express-validator');
const ApiResponse = require('../utils/responseFormatter');

const handleValidation = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    const formattedErrors = errors.array().map(e => ({ field: e.path, message: e.msg }));
    return ApiResponse.error(res, "Validation failed", formattedErrors, 422);
  }
  next();
};

const validateRegister = [
  body('fullName').trim().notEmpty().withMessage('Full name is required').isLength({ min: 2, max: 50 }).withMessage('Name must be 2-50 characters'),
  body('mobileNumber').trim().notEmpty().withMessage('Mobile number is required').matches(/^[6-9]\d{9}$/).withMessage('Enter a valid 10-digit Indian mobile number'),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
  handleValidation,
];

const validateLogin = [
  body('identifier').trim().notEmpty().withMessage('Email or mobile number is required'),
  body('password').notEmpty().withMessage('Password is required'),
  handleValidation,
];

const validateCropRecommend = [
  body('nitrogen').isFloat({ min: 0, max: 140 }).withMessage('Nitrogen must be 0-140'),
  body('phosphorus').isFloat({ min: 0, max: 145 }).withMessage('Phosphorus must be 0-145'),
  body('potassium').isFloat({ min: 0, max: 205 }).withMessage('Potassium must be 0-205'),
  body('ph').isFloat({ min: 0, max: 14 }).withMessage('pH must be 0-14'),
  body('rainfall').isFloat({ min: 0, max: 3000 }).withMessage('Rainfall must be 0-3000mm'),
  body('temperature').isFloat({ min: -10, max: 60 }).withMessage('Temperature must be -10 to 60°C'),
  body('humidity').isFloat({ min: 0, max: 100 }).withMessage('Humidity must be 0-100%'),
  handleValidation,
];

const validateWeatherRisk = [
  body('location').trim().notEmpty().withMessage('Location is required').isLength({ min: 2 }).withMessage('Enter a valid location name'),
  handleValidation,
];

const validateMarketInsights = [
  body('crop').trim().notEmpty().withMessage('Crop name is required'),
  body('location').trim().notEmpty().withMessage('Location is required'),
  handleValidation,
];

const validateStrategy = [
  body('goal').trim().notEmpty().withMessage('Farming goal is required').isLength({ min: 5 }).withMessage('Goal must be at least 5 characters'),
  handleValidation,
];

module.exports = {
  validateRegister,
  validateLogin,
  validateCropRecommend,
  validateWeatherRisk,
  validateMarketInsights,
  validateStrategy,
};
