require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const compression = require('compression');

const mongoSanitize = require('express-mongo-sanitize');


const authRoutes = require('./routes/authRoutes');
const cropRoutes = require('./routes/cropRoutes');
const weatherRoutes = require('./routes/weatherRoutes');
const visionRoutes = require('./routes/visionRoutes');
const marketRoutes = require('./routes/marketRoutes');
const strategistRoutes = require('./routes/strategistRoutes');
const dashboardRoutes = require('./routes/dashboardRoutes');
const errorHandler = require('./middleware/errorHandler');
const logger = require('./utils/logger');
const ApiResponse = require('./utils/responseFormatter');

const app = express();

// Security Middleware
app.use(helmet({ crossOriginResourcePolicy: { policy: 'cross-origin' } }));
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true,
}));

// Body Parser
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));


app.use(mongoSanitize());
app.use(compression());

// Logging Middleware
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) } }));

// Serve uploaded images statically
app.use('/uploads', express.static('uploads'));

// Rate limiting
const authLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 20, message: { message: 'Too many attempts, try again in 15 minutes' } });
const apiLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 200 });

// Health check
app.get('/health', (req, res) => ApiResponse.success(res, 'Server is running healthily', { timestamp: new Date().toISOString() }));

// Routes
app.use('/api/auth', authLimiter, authRoutes);
app.use('/api/crop', apiLimiter, cropRoutes);
app.use('/api/weather', apiLimiter, weatherRoutes);
app.use('/api/vision', apiLimiter, visionRoutes);
app.use('/api/market', apiLimiter, marketRoutes);
app.use('/api/strategist', apiLimiter, strategistRoutes);
app.use('/api/dashboard', apiLimiter, dashboardRoutes);

// 404
app.use((req, res) => ApiResponse.error(res, `Route ${req.originalUrl} not found`, null, 404));

// Error handler
app.use(errorHandler);

module.exports = app;