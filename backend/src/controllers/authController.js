const jwt = require('jsonwebtoken');
const { userRepo } = require('../repositories');
const ApiResponse = require('../utils/responseFormatter');

const generateToken = (userId) => jwt.sign({ id: userId }, process.env.JWT_SECRET, { expiresIn: process.env.JWT_EXPIRES_IN || '7d' });

const register = async (req, res, next) => {
  try {
    const { fullName, mobileNumber, password, email } = req.body;
    const existing = await userRepo.findOne({ mobileNumber });
    if (existing) return ApiResponse.error(res, 'Mobile number already registered.', null, 409);
    
    const user = await userRepo.create({ fullName, mobileNumber, password, email: email || '' });
    const token = generateToken(user._id);
    
    return ApiResponse.success(res, 'Registration successful', { token, user: user.toSafeObject() }, 201);
  } catch (err) { next(err); }
};

const login = async (req, res, next) => {
  try {
    const { identifier, password } = req.body;
    const user = await userRepo.findByIdentifier(identifier);
    if (!user) return ApiResponse.error(res, 'Invalid credentials.', null, 401);
    
    const isMatch = await user.comparePassword(password);
    if (!isMatch) return ApiResponse.error(res, 'Invalid credentials.', null, 401);
    
    const token = generateToken(user._id);
    return ApiResponse.success(res, 'Login successful', { token, user: user.toSafeObject() });
  } catch (err) { next(err); }
};

const getProfile = async (req, res) => {
  return ApiResponse.success(res, 'Profile retrieved', { user: req.user.toSafeObject ? req.user.toSafeObject() : req.user });
};

module.exports = { register, login, getProfile };