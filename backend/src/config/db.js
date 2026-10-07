const mongoose = require('mongoose');

let isConnected = false;

const logger = require('../utils/logger');

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI, {
      serverSelectionTimeoutMS: 4000,
      socketTimeoutMS: 4000,
    });
    isConnected = true;
    logger.info('MongoDB connected');
    return true;
  } catch (err) {
    isConnected = false;
    logger.error(`❌ MongoDB failed: ${err.message}`);
    logger.warn('Running without DB — data will not persist');
    return false;
  }
};

const getConnectionStatus = () => isConnected;

module.exports = { connectDB, getConnectionStatus };