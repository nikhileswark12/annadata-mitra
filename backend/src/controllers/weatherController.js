const axios = require('axios');
const { weatherRepo } = require('../repositories');
const ApiResponse = require('../utils/responseFormatter');
const logger = require('../utils/logger');

const getRisk = async (req, res, next) => {
  try {
    const { location, crop } = req.body;
    
    let weatherData;

    try {
      const payload = crop ? { location, crop } : { location };
      const flaskRes = await axios.post(`${process.env.PYTHON_SERVICE_URL}/weather-risk`, payload, { timeout: 8000 });
      weatherData = flaskRes.data.data;
    } catch (flaskErr) {
      logger.warn('Weather AI service error', { error: flaskErr.message });
      if (flaskErr.response && flaskErr.response.status < 500) {
        return res.status(flaskErr.response.status).json(flaskErr.response.data);
      }
      return ApiResponse.error(res, 'Weather AI service unavailable', null, 503);
    }

    if (req.user) {
      weatherRepo.create({ 
        userId: req.user._id, 
        location: weatherData.location,
        temperature: weatherData.temperature,
        humidity: weatherData.humidity,
        rainfall: weatherData.rainfall,
        windSpeed: weatherData.windSpeed,
        condition: weatherData.condition,
        risks: weatherData.risks
      }).catch(e => logger.error('DB save failed', e));
    }

    return ApiResponse.success(res, 'Weather risk analysis generated', weatherData);
  } catch (err) { next(err); }
};

const history = async (req, res, next) => {
  try {
    const logs = await weatherRepo.find({ userId: req.user._id });
    return ApiResponse.success(res, 'Weather history retrieved', { logs });
  } catch (err) { next(err); }
};

module.exports = { getRisk, history };