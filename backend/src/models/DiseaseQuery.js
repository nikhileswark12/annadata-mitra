const mongoose = require('mongoose');

const diseaseQuerySchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  imagePath: { type: String, required: true },
  disease: { type: String, required: true },
  confidence: { type: Number, required: true, min: 0, max: 100 },
  severity: { type: String, enum: ['Low', 'Medium', 'High'], required: true },
  description: { type: String },
  treatment: { type: String },
  source: { type: String, enum: ['ml-model', 'synthetic', 'manual'], default: 'synthetic' }
}, { timestamps: true });

// TTL index to automatically delete old queries after 90 days to save storage
diseaseQuerySchema.index({ createdAt: 1 }, { expireAfterSeconds: 90 * 24 * 60 * 60 });

module.exports = mongoose.model('DiseaseQuery', diseaseQuerySchema);
