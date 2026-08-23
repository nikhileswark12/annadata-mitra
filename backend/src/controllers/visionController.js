const path = require('path');
const crypto = require('crypto');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const { diseaseRepo } = require('../repositories');
const ApiResponse = require('../utils/responseFormatter');
const logger = require('../utils/logger');

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, path.join(__dirname, '../../uploads')),
  filename: (req, file, cb) => cb(null, `${crypto.randomUUID()}${path.extname(file.originalname).toLowerCase()}`),
});

const fileFilter = (req, file, cb) => {
  const allowed = ['image/jpeg', 'image/jpg', 'image/png'];
  if (allowed.includes(file.mimetype)) cb(null, true);
  else cb(new Error('INVALID_FILE_TYPE'), false);
};

const upload = multer({ storage, fileFilter, limits: { fileSize: 5 * 1024 * 1024 } });

const analyze = async (req, res, next) => {
  try {
    if (!req.file) return ApiResponse.error(res, 'Please upload a plant leaf image.', null, 400);

    const imagePath = `/uploads/${req.file.filename}`;
    let diagnosis;

    try {
      const formData = new FormData();
      formData.append('image', fs.createReadStream(req.file.path));
      const flaskRes = await axios.post(`${process.env.PYTHON_SERVICE_URL}/disease-detect`, formData, {
        headers: formData.getHeaders(), timeout: 30000,
      });
      diagnosis = flaskRes.data.data;
    } catch (flaskErr) {
      logger.warn('Vision AI service error', { error: flaskErr.message });
      if (flaskErr.response && flaskErr.response.status < 500) {
        return res.status(flaskErr.response.status).json(flaskErr.response.data);
      }
      return ApiResponse.error(res, 'Vision AI service unavailable', null, 503);
    }

    if (req.user) {
      diseaseRepo.create({ 
        userId: req.user._id, 
        imagePath, 
        disease: diagnosis.disease,
        confidence: diagnosis.confidence,
        severity: diagnosis.severity,
        description: diagnosis.description,
        treatment: diagnosis.treatment
      }).catch(e => logger.error('DB save failed', e));
    }

    return ApiResponse.success(res, 'Diagnosis completed', { ...diagnosis, imagePath });
  } catch (err) { next(err); }
};

const history = async (req, res, next) => {
  try {
    const queries = await diseaseRepo.find({ userId: req.user._id });
    return ApiResponse.success(res, 'Disease detection history retrieved', { queries });
  } catch (err) { next(err); }
};

module.exports = { upload, analyze, history };