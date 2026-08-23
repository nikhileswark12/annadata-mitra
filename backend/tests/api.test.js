const request = require('supertest');
const app = require('../src/app');

describe('API Health Check', () => {
  it('should return 200 OK', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toEqual(200);
    expect(res.body).toHaveProperty('status', 'success');
    expect(res.body).toHaveProperty('message', 'Server is running healthily');
  });
});

describe('404 Not Found', () => {
  it('should return 404 for unknown routes', async () => {
    const res = await request(app).get('/api/unknown');
    expect(res.statusCode).toEqual(404);
    expect(res.body).toHaveProperty('status', 'error');
  });
});
