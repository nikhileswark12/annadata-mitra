const axios = require('axios');
const { marketRepo } = require('../repositories');
const ApiResponse = require('../utils/responseFormatter');
const logger = require('../utils/logger');

const getInsights = async (req, res, next) => {
  try {
    const { crop, location, quantity } = req.body;
    let result;

    try {
      const flaskRes = await axios.post(`${process.env.PYTHON_SERVICE_URL}/market-insights`, { crop, location, quantity }, { timeout: 10000 });
      result = flaskRes.data.data;
      
      // Inject missing fields from request
      result.crop = crop;
      result.location = location;
      
      // Calculate totalValue if quantity was provided
      if (quantity && result.currentPrice) {
        result.totalValue = Math.round((quantity / 100) * result.currentPrice);
      }
    } catch (flaskErr) {
      logger.warn('Market AI service error', { error: flaskErr.message });
      if (flaskErr.response && flaskErr.response.status < 500) {
        return res.status(flaskErr.response.status).json(flaskErr.response.data);
      }
      return ApiResponse.error(res, 'Market AI service unavailable', null, 503);
    }

    if (req.user) {
      marketRepo.create({ 
        userId: req.user._id, 
        ...result, 
        quantity 
      }).catch(e => logger.error('DB save failed', e));
    }

    return ApiResponse.success(res, 'Market insights generated', result);
  } catch (err) { next(err); }
};

const history = async (req, res, next) => {
  try {
    const searches = await marketRepo.find({ userId: req.user._id });
    return ApiResponse.success(res, 'Market search history retrieved', { searches });
  } catch (err) { next(err); }
};

module.exports = { getInsights, history };