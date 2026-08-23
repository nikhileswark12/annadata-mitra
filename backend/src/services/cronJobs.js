const cron = require('node-cron');
const { weatherRepo } = require('../repositories');
const axios = require('axios');
const logger = require('../utils/logger');

// Fetch weather data every 6 hours (0 0,6,12,18 * * *)
const startCronJobs = () => {
  cron.schedule('0 */6 * * *', async () => {
    logger.info('Running scheduled weather update job');
    try {
      // Logic to find all active unique locations and update their weather cache
      // This is a placeholder for the actual implementation which would iterate
      // through farms/users, get their location, and call OpenWeatherMap
      logger.info('Weather update job completed successfully');
    } catch (error) {
      logger.error('Error in scheduled weather update job', { error: error.message });
    }
  });
  logger.info('Cron jobs scheduled');
};

module.exports = { startCronJobs };
