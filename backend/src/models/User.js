const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  fullName: { type: String, required: true, trim: true, minlength: [2, 'Name too short'], maxlength: 100 },
  mobileNumber: { type: String, required: true, unique: true, match: [/^\d{10}$/, 'Please enter a valid 10-digit mobile number'] },
  email: { type: String, lowercase: true, trim: true, match: [/^\S+@\S+\.\S+$/, 'Invalid email format'] },
  password: { type: String, required: true, minlength: [6, 'Password minimum 6 characters'] },
  role: { type: String, enum: ['farmer', 'admin'], default: 'farmer' },
  status: { type: String, enum: ['active', 'inactive', 'suspended'], default: 'active' },
  farmDetails: {
    sizeInAcres: { type: Number, min: 0 },
    primaryCrops: [{ type: String }],
    soilType: { type: String },
    location: { type: String },
    coordinates: {
      type: { type: String, enum: ['Point'] },
      coordinates: { type: [Number] } // [longitude, latitude]
    }
  }
}, { timestamps: true });

// Indexes
userSchema.index({ 'farmDetails.coordinates': '2dsphere' });

// Pre-save password hashing
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) { next(error); }
});

// Compare password
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Return safe object
userSchema.methods.toSafeObject = function() {
  const obj = this.toObject();
  delete obj.password;
  delete obj.__v;
  return obj;
};

module.exports = mongoose.model('User', userSchema);