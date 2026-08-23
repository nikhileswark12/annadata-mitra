const request = require('supertest');
const mongoose = require('mongoose');
const app = require('../src/app');

describe('AI Services Mock Integrations', () => {
  let token;

  beforeAll(async () => {
    if (mongoose.connection.readyState === 0) {
      await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/annadata-mitra-test');
    }
    
    // Create user and get token
    await mongoose.connection.collection('users').deleteMany({});
    const res = await request(app).post('/api/auth/register').send({
      fullName: 'AI Tester',
      mobileNumber: '9988776655',
      password: 'password123',
      farmDetails: { sizeInAcres: 5 }
    });
    token = res.body.data.token;
  });

  afterAll(async () => {
    await mongoose.connection.close();
  });

  describe('POST /api/crop/recommend', () => {
    it('should return mock rule-based crop recommendations', async () => {
      const res = await request(app).post('/api/crop/recommend')
        .set('Authorization', `Bearer ${token}`)
        .send({
          nitrogen: 65,
          phosphorus: 35,
          potassium: 35,
          ph: 6.5,
          rainfall: 200,
          temperature: 28,
          humidity: 80,
          location: 'Gujarat'
        });
      
      expect(res.statusCode).toEqual(200);
      expect(res.body.status).toEqual('success');
      expect(res.body.data.source).toEqual('rule-based');
      expect(Array.isArray(res.body.data.recommendations)).toBe(true);
      expect(res.body.data.recommendations.length).toBeGreaterThan(0);
      expect(res.body.data.recommendations[0]).toHaveProperty('crop');
      expect(res.body.data.recommendations[0]).toHaveProperty('confidence');
      expect(res.body.data.recommendations[0]).toHaveProperty('reasoning');
    });
  });

  describe('POST /api/weather/risk', () => {
    it('should return synthetic weather risk analysis', async () => {
      const res = await request(app).post('/api/weather/risk')
        .set('Authorization', `Bearer ${token}`)
        .send({ location: 'Pune' });

      expect(res.statusCode).toEqual(200);
      expect(res.body.status).toEqual('success');
      expect(res.body.data.source).toEqual('synthetic');
      expect(res.body.data).toHaveProperty('temperature');
      expect(res.body.data).toHaveProperty('humidity');
      expect(Array.isArray(res.body.data.risks)).toBe(true);
    });
  });

  describe('POST /api/market/insights', () => {
    it('should return synthetic market insights', async () => {
      const res = await request(app).post('/api/market/insights')
        .set('Authorization', `Bearer ${token}`)
        .send({
          crop: 'cotton',
          location: 'Maharashtra',
          quantity: 100
        });

      expect(res.statusCode).toEqual(200);
      expect(res.body.status).toEqual('success');
      expect(res.body.data.source).toEqual('synthetic');
      expect(res.body.data).toHaveProperty('currentPrice');
      expect(res.body.data).toHaveProperty('predictedPrice');
      expect(res.body.data).toHaveProperty('advice');
      expect(Array.isArray(res.body.data.markets)).toBe(true);
    });
  });

  describe('POST /api/strategist/generate', () => {
    it('should return rule-based farming strategy', async () => {
      const res = await request(app).post('/api/strategist/generate')
        .set('Authorization', `Bearer ${token}`)
        .send({ goal: 'I want to maximize profit for wheat in Punjab' });

      expect(res.statusCode).toEqual(200);
      expect(res.body.status).toEqual('success');
      expect(res.body.data.source).toEqual('rule-engine');
      expect(res.body.data).toHaveProperty('cropAdvice');
      expect(res.body.data).toHaveProperty('marketTiming');
      expect(Array.isArray(res.body.data.actions)).toBe(true);
    });
  });
});
