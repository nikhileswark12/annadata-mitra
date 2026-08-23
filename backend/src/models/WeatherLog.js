const mongoose = require('mongoose');

const weatherLogSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true, index: true },
  location: { type: String, required: true, index: true },
  temperature: { type: Number, required: true },
  humidity: { type: Number, required: true },
  rainfall: { type: Number, required: true },
  windSpeed: { type: Number, required: true },
  condition: { type: String, required: true },
  risks: [{
    type: { type: String, required: true }, // Not using 'type' alone as schema type, this is fine in nested obj
    severity: { type: String, enum: ['Low', 'Medium', 'High'], required: true },
    message: { type: String },
    recommendation: { type: String }
  }]
}, { timestamps: true });

// TTL index to automatically delete old weather logs after 30 days
weatherLogSchema.index({ createdAt: 1 }, { expireAfterSeconds: 30 * 24 * 60 * 60 });

module.exports = mongoose.model('WeatherLog', weatherLogSchema);
