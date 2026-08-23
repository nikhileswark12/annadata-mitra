const ApiResponse = require('../utils/responseFormatter');
const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
  logger.error(`${req.method} ${req.path} - ${err.message}`, { stack: err.stack, body: req.body });

  // Multer errors
  if (err.code === 'LIMIT_FILE_SIZE') return ApiResponse.error(res, 'File too large. Maximum 5MB allowed.', null, 413);
  if (err.code === 'LIMIT_UNEXPECTED_FILE') return ApiResponse.error(res, 'Unexpected file field.', null, 400);
  if (err.message === 'INVALID_FILE_TYPE') return ApiResponse.error(res, 'Only JPG, PNG, JPEG images are allowed.', null, 400);

  // Mongoose errors
  if (err.name === 'ValidationError') {
    const messages = Object.values(err.errors).map(e => ({ field: e.path, message: e.message }));
    return ApiResponse.error(res, 'Validation Error', messages, 422);
  }
  if (err.code === 11000) {
    const field = Object.keys(err.keyValue)[0];
    return ApiResponse.error(res, `${field} already registered.`, null, 409);
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') return ApiResponse.error(res, 'Invalid token.', null, 401);
  if (err.name === 'TokenExpiredError') return ApiResponse.error(res, 'Token expired.', null, 401);

  // Default error
  return ApiResponse.error(res, err.message || 'Internal server error', null, err.status || 500);
};

module.exports = errorHandler;
