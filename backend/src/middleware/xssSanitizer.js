const sanitizeHtml = require('sanitize-html');

const sanitizeObject = (obj) => {
  if (obj && typeof obj === 'object') {
    Object.keys(obj).forEach((key) => {
      if (typeof obj[key] === 'string') {
        obj[key] = sanitizeHtml(obj[key], {
          allowedTags: [],
          allowedAttributes: {}
        });
      } else if (typeof obj[key] === 'object') {
        sanitizeObject(obj[key]);
      }
    });
  }
};

const xssSanitizer = (req, res, next) => {
  if (req.body) sanitizeObject(req.body);
  if (req.query) sanitizeObject(req.query);
  if (req.params) sanitizeObject(req.params);
  next();
};

module.exports = xssSanitizer;
