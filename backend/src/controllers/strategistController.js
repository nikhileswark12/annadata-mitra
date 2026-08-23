const axios = require('axios');
const { strategyRepo } = require('../repositories');
const ApiResponse = require('../utils/responseFormatter');

const generate = async (req, res, next) => {
  try {
    const { goal, location, crop } = req.body;
    
    // Proxy request to Python AI Service
    let strategyData;
    try {
      const response = await axios.post(`${process.env.PYTHON_SERVICE_URL}/strategist-plan`, {
        goal: goal || "",
        location: location || "",
        crop: crop || ""
      });
      strategyData = response.data?.data;
    } catch (flaskErr) {
      console.error('Strategist AI service error:', flaskErr.message);
      if (flaskErr.response && flaskErr.response.status < 500) {
        return res.status(flaskErr.response.status).json(flaskErr.response.data);
      }
      return ApiResponse.error(res, 'Strategist AI service unavailable', null, 503);
    }

    if (req.user && strategyData) {
      strategyRepo.create({ userId: req.user._id, ...strategyData }).catch(e => console.error('DB save:', e.message));
    }

    return ApiResponse.success(res, 'Strategy generated', strategyData);
  } catch (err) { next(err); }
};

const history = async (req, res, next) => {
  try {
    const strategies = await strategyRepo.find({ userId: req.user._id });
    return ApiResponse.success(res, 'Strategy history retrieved', { strategies });
  } catch (err) { next(err); }
};

module.exports = { generate, history };
