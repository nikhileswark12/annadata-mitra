const xssSanitizer = require('../src/middleware/xssSanitizer');
const errorHandler = require('../src/middleware/errorHandler');

describe('Middleware Tests', () => {
  describe('xssSanitizer', () => {
    it('should sanitize req.body, req.query, and req.params', () => {
      const req = {
        body: { text: '<script>alert("xss")</script>Hello' },
        query: { search: '<img src=x onerror=alert(1)>' },
        params: { id: '<b>123</b>' }
      };
      const next = jest.fn();

      xssSanitizer(req, {}, next);

      expect(req.body.text).toBe('Hello');
      expect(req.query.search).toBe('');
      expect(req.params.id).toBe('123');
      expect(next).toHaveBeenCalled();
    });
  });

  describe('errorHandler', () => {
    it('should format mongoose validation errors', () => {
      const err = { 
        name: 'ValidationError', 
        message: 'Test validation error',
        errors: {
          field1: { path: 'field1', message: 'is required' }
        }
      };
      const req = {};
      const res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      };
      const next = jest.fn();

      errorHandler(err, req, res, next);

      expect(res.status).toHaveBeenCalledWith(422);
      expect(res.json).toHaveBeenCalledWith(expect.objectContaining({
        status: 'error',
        message: 'Validation Error',
        errors: [{ field: 'field1', message: 'is required' }]
      }));
    });

    it('should catch generic errors', () => {
      const err = new Error('Something broke');
      const req = {};
      const res = {
        status: jest.fn().mockReturnThis(),
        json: jest.fn()
      };
      const next = jest.fn();

      errorHandler(err, req, res, next);

      expect(res.status).toHaveBeenCalledWith(500);
      expect(res.json).toHaveBeenCalledWith(expect.objectContaining({
        status: 'error',
        message: 'Something broke'
      }));
    });
  });
});
