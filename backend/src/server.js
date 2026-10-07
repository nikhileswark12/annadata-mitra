require('dotenv').config();
const app = require('./app');
const { connectDB } = require('./config/db');

const PORT = process.env.PORT || 5000;

const logger = require('./utils/logger');

// Prevent any escaped promise from crashing the process
process.on('unhandledRejection', (reason) => {
  const msg = reason?.message || String(reason);
  if (
    msg.includes('before initial connection') ||
    msg.includes('bufferCommands') ||
    msg.includes('buffering timed out') ||
    msg.includes('ECONNREFUSED')
  ) return; // expected when MongoDB is offline
  logger.error(`[Unhandled Rejection] ${msg}`);
});

const start = async () => {
  const dbConnected = await connectDB();
  if (!dbConnected && process.env.NODE_ENV === 'production') {
    logger.error('Fatal: MongoDB is required in production. Server startup aborted.');
    process.exit(1);
  }

  app.listen(PORT, () => {
    logger.info(`🚀 Server on http://localhost:${PORT}`);
    logger.info(`🤖 AI service: ${process.env.PYTHON_SERVICE_URL}`);
  });
};

start().catch((err) => {
  logger.error(`Fatal: ${err.message}`);
  process.exit(1);
});