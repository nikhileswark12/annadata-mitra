/**
 * Standard API response formatter
 */
class ApiResponse {
  constructor(success, messageOrError, dataOrDetails = null) {
    this.success = success;
    if (success) {
      this.message = messageOrError;
      if (dataOrDetails) this.data = dataOrDetails;
    } else {
      this.error = messageOrError;
      if (dataOrDetails) this.details = dataOrDetails;
    }
    this.timestamp = new Date().toISOString();
  }

  static success(res, message, data = null, statusCode = 200) {
    return res.status(statusCode).json(new ApiResponse(true, message, data));
  }

  static error(res, message, errors = null, statusCode = 500) {
    return res.status(statusCode).json(new ApiResponse(false, message, errors));
  }
}

module.exports = ApiResponse;
