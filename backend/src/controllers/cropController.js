const axios = require('axios');
const { cropRepo } = require('../repositories');
const ApiResponse = require('../utils/responseFormatter');
const logger = require('../utils/logger');


const recommend = async (req, res, next) => {
  try {
    const { nitrogen, phosphorus, potassium, ph, rainfall, temperature, humidity, location } = req.body;
    const inputs = { nitrogen: +nitrogen, phosphorus: +phosphorus, potassium: +potassium, ph: +ph, rainfall: +rainfall, temperature: +temperature, humidity: +humidity, location };

    let recommendations;
    let source;

    try {
      const flaskRes = await axios.post(`${process.env.PYTHON_SERVICE_URL}/crop-recommend`, inputs, { timeout: 8000 });
      recommendations = flaskRes.data.data.recommendations;
      source = flaskRes.data.data.source || 'ml-model';
    } catch (flaskErr) {
      logger.warn('Crop AI service error', { error: flaskErr.message });
      if (flaskErr.response && flaskErr.response.status < 500) {
        return res.status(flaskErr.response.status).json(flaskErr.response.data);
      }
      return ApiResponse.error(res, 'Crop AI service unavailable', null, 503);
    }

    if (req.user) {
      cropRepo.create({ userId: req.user._id, inputs, recommendations }).catch(e => logger.error('DB save failed', e));
    }

    const message = 'Crop recommendations generated';
    return ApiResponse.success(res, message, { recommendations, source });
  } catch (err) { next(err); }
};

const history = async (req, res, next) => {
  try {
    const plans = await cropRepo.find({ userId: req.user._id });
    return ApiResponse.success(res, 'Crop planning history retrieved', { plans });
  } catch (err) { next(err); }
};

module.exports = { recommend, history };