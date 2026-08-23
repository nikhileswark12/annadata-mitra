const jwt = require('jsonwebtoken');
const User = require('../models/User');

const authMiddleware = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ message: 'No token provided' });
    }
    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    try {
      const user = await User.findById(decoded.id)
        .select('-password')
        .maxTimeMS(3000);
      if (user) {
        req.user = user;
        return next();
      }
      // User not in DB — allow in dev mode for testing without MongoDB
      if (process.env.NODE_ENV === 'development') {
        req.user = {
          _id: decoded.id,
          fullName: 'Dev User',
          mobileNumber: '0000000000'
        };
        return next();
      }
      return res.status(401).json({ message: 'User not found' });
    } catch (dbErr) {
      if (process.env.NODE_ENV === 'development') {
        req.user = {
          _id: decoded.id,
          fullName: 'Dev User',
          mobileNumber: '0000000000'
        };
        return next();
      }
      return res.status(503).json({ message: 'Database unavailable' });
    }
  } catch (err) {
    if (err.name === 'TokenExpiredError')
      return res.status(401).json({ message: 'Token expired' });
    return res.status(401).json({ message: 'Invalid token' });
  }
};

module.exports = authMiddleware;
