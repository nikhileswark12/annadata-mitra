const request = require('supertest');
const mongoose = require('mongoose');
const axios = require('axios');
const app = require('../src/app');

jest.mock('axios');

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

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('POST /api/crop/recommend', () => {
    it('should return mock rule-based crop recommendations', async () => {
      axios.post.mockResolvedValueOnce({
        data: {
          success: true,
          data: {
            source: 'rule-based',
            recommendations: [
              { crop: 'wheat', confidence: 90, reasoning: 'Mock reasoning' }
            ]
          }
        }
      });

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
      expect(res.body.success).toEqual(true);
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
      axios.post.mockResolvedValueOnce({
        data: {
          success: true,
          data: {
            source: 'synthetic',
            temperature: 25,
            humidity: 60,
            rainfall: 10,
            windSpeed: 15,
            condition: 'Clear',
            location: 'Pune',
            risks: [{ type: 'Heat', severity: 'Low', description: 'Mock risk' }]
          }
        }
      });

      const res = await request(app).post('/api/weather/risk')
        .set('Authorization', `Bearer ${token}`)
        .send({ location: 'Pune' });

      expect(res.statusCode).toEqual(200);
      expect(res.body.success).toEqual(true);
      expect(res.body.data.source).toEqual('synthetic');
      expect(res.body.data).toHaveProperty('temperature');
      expect(res.body.data).toHaveProperty('humidity');
      expect(Array.isArray(res.body.data.risks)).toBe(true);
    });
  });

  describe('POST /api/market/insights', () => {
    it('should return synthetic market insights', async () => {
      axios.post.mockResolvedValueOnce({
        data: {
          success: true,
          data: {
            source: 'synthetic',
            currentPrice: 5000,
            predictedPrice: 5200,
            advice: 'Wait',
            trendWatch: 'Upward',
            state: 'Maharashtra',
            markets: [{ name: 'Pune Market', distance: 10, price: 5050, trend: 'Up' }]
          }
        }
      });

      const res = await request(app).post('/api/market/insights')
        .set('Authorization', `Bearer ${token}`)
        .send({
          crop: 'cotton',
          location: 'Maharashtra',
          quantity: 100
        });

      expect(res.statusCode).toEqual(200);
      expect(res.body.success).toEqual(true);
      expect(res.body.data.source).toEqual('synthetic');
      expect(res.body.data).toHaveProperty('currentPrice');
      expect(res.body.data).toHaveProperty('predictedPrice');
      expect(res.body.data).toHaveProperty('advice');
      expect(Array.isArray(res.body.data.markets)).toBe(true);
    });
  });

  describe('POST /api/strategist/generate', () => {
    it('should return rule-based farming strategy', async () => {
      axios.post.mockResolvedValueOnce({
        data: {
          success: true,
          data: {
            source: 'rule-engine',
            cropAdvice: 'Mock advice',
            marketTiming: 'Mock timing',
            weatherRisk: 'Low',
            farmAdvisory: 'Test advisory',
            season: 'Rabi',
            crop: 'wheat',
            location: 'Punjab',
            goal: 'Maximize profit',
            confidence: 85,
            actions: ['Mock action']
          }
        }
      });

      const res = await request(app).post('/api/strategist/generate')
        .set('Authorization', `Bearer ${token}`)
        .send({ goal: 'I want to maximize profit for wheat in Punjab' });

      expect(res.statusCode).toEqual(200);
      expect(res.body.success).toEqual(true);
      expect(res.body.data.source).toEqual('rule-engine');
      expect(res.body.data).toHaveProperty('cropAdvice');
      expect(res.body.data).toHaveProperty('marketTiming');
      expect(Array.isArray(res.body.data.actions)).toBe(true);
    });
  });
});
