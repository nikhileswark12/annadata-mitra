const mongoose = require('mongoose');

const cropPlanSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  inputs: {
    nitrogen: { type: Number, required: true, min: 0, max: 200 },
    phosphorus: { type: Number, required: true, min: 0, max: 200 },
    potassium: { type: Number, required: true, min: 0, max: 200 },
    ph: { type: Number, required: true, min: 0, max: 14 },
    rainfall: { type: Number, required: true, min: 0 },
    temperature: { type: Number, required: true },
    humidity: { type: Number, required: true, min: 0, max: 100 },
    location: { type: String, required: true, trim: true }
  },
  recommendations: [{
    crop: { type: String, required: true },
    confidence: { type: Number, required: true, min: 0, max: 100 },
    reasoning: { type: String },
    icon: { type: String }
  }],
  status: { type: String, enum: ['planned', 'planted', 'harvested', 'cancelled'], default: 'planned' }
}, { timestamps: true });

// Add TTL index to clean up old plans if they are not updated
cropPlanSchema.index({ createdAt: 1 }, { expireAfterSeconds: 365 * 24 * 60 * 60 }); // 1 year TTL

module.exports = mongoose.model('CropPlan', cropPlanSchema);
