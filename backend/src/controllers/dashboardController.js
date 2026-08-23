const { cropRepo, diseaseRepo, marketRepo, weatherRepo } = require('../repositories');
const ApiResponse = require('../utils/responseFormatter');

const getStats = async (req, res, next) => {
  try {
    const userId = req.user._id;

    const [cropCount, weatherCount, diseaseCount, bestMarket, recentCrop, recentWeather, recentMarket] = await Promise.all([
      cropRepo.count({ userId }),
      weatherRepo.count({ userId }),
      diseaseRepo.count({ userId }),
      marketRepo.model.findOne({ userId }).sort({ currentPrice: -1 }).lean(),
      cropRepo.model.findOne({ userId }).sort({ createdAt: -1 }).lean(),
      weatherRepo.model.findOne({ userId }).sort({ createdAt: -1 }).lean(),
      marketRepo.model.findOne({ userId }).sort({ createdAt: -1 }).lean(),
    ]);

    const activities = [];
    if (recentMarket) activities.push({ text: `${recentMarket.crop} market trend checked for ${recentMarket.location}`, time: recentMarket.createdAt });
    if (recentCrop) activities.push({ text: `Crop planning done — top pick: ${recentCrop.recommendations?.[0]?.crop || 'N/A'}`, time: recentCrop.createdAt });
    if (recentWeather) activities.push({ text: `Weather risk reviewed for ${recentWeather.location}`, time: recentWeather.createdAt });
    activities.sort((a, b) => new Date(b.time) - new Date(a.time));

    return ApiResponse.success(res, 'Dashboard stats retrieved', {
      cropSuggestions: cropCount,
      weatherAlerts: weatherCount,
      diseaseScans: diseaseCount,
      bestMarketPrice: bestMarket ? { price: bestMarket.currentPrice, location: bestMarket.location, crop: bestMarket.crop } : null,
      recentActivities: activities.slice(0, 5)
    });
  } catch (err) { next(err); }
};

module.exports = { getStats };
