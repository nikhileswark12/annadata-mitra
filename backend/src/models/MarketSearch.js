const mongoose = require('mongoose');

const marketSearchSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  crop: { type: String, required: true, index: true, lowercase: true, trim: true },
  location: { type: String, required: true, trim: true },
  state: { type: String, required: true, lowercase: true, index: true },
  quantity: { type: Number, min: 0 },
  currentPrice: { type: Number, required: true },
  predictedPrice: { type: Number },
  advice: { type: String, enum: ['Wait', 'Sell Now', 'Monitor'], required: true },
  trendWatch: { type: String, enum: ['Upward', 'Downward', 'Stable'], required: true },
  demandInsight: { type: String },
  totalValue: { type: Number },
  forecastDays: { type: Number, default: 7 },
  markets: [{
    name: { type: String, required: true },
    price: { type: Number, required: true },
    trend: { type: String, enum: ['Up', 'Stable', 'Down'], required: true },
    distance: { type: String }
  }]
}, { timestamps: true });

// TTL index for market searches (prices change daily, no need to keep old logs > 30 days)
marketSearchSchema.index({ createdAt: 1 }, { expireAfterSeconds: 30 * 24 * 60 * 60 });

module.exports = mongoose.model('MarketSearch', marketSearchSchema);
