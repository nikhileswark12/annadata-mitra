const mongoose = require('mongoose');

const strategySchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  goal: { type: String, required: true, trim: true },
  crop: { type: String, required: true },
  location: { type: String, required: true },
  season: { type: String, enum: ['Kharif', 'Rabi', 'Zaid'], required: true },
  cropAdvice: { type: String, required: true },
  marketTiming: { type: String, required: true },
  weatherRisk: { type: String, required: true },
  farmAdvisory: { type: String, required: true },
  actions: [{ type: String }],
  confidence: { type: Number, required: true, min: 0, max: 100 },
  source: { type: String, enum: ['rule-engine', 'ml-model'], default: 'rule-engine' },
  status: { type: String, enum: ['active', 'completed', 'archived'], default: 'active' }
}, { timestamps: true });

// TTL index for inactive strategies
strategySchema.index({ createdAt: 1 }, { expireAfterSeconds: 365 * 24 * 60 * 60 });

module.exports = mongoose.model('Strategy', strategySchema);
