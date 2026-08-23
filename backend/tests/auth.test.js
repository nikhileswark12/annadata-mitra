const request = require('supertest');
const mongoose = require('mongoose');
const app = require('../src/app');
const User = require('../src/models/User');

describe('Authentication Flow', () => {
  let token;
  const testUser = {
    fullName: 'Test Farmer',
    mobileNumber: '9998887776',
    password: 'password123',
    farmDetails: {
      sizeInAcres: 5,
    }
  };

  beforeAll(async () => {
    // Connect to database is handled in app.js or server.js ? 
    // Actually, app.js doesn't connect. server.js connects.
    // If not connected, connect here.
    if (mongoose.connection.readyState === 0) {
      await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/annadata-mitra-test');
    }
    await User.deleteMany({});
  });

  afterAll(async () => {
    await User.deleteMany({});
    await mongoose.connection.close();
  });

  it('should register a new user', async () => {
    const res = await request(app).post('/api/auth/register').send(testUser);
    expect(res.statusCode).toEqual(201);
    expect(res.body.data.user.mobileNumber).toEqual(testUser.mobileNumber);
    expect(res.body.data.token).toBeDefined();
  });

  it('should login the user and return JWT', async () => {
    const res = await request(app).post('/api/auth/login').send({
      identifier: testUser.mobileNumber,
      password: testUser.password
    });
    expect(res.statusCode).toEqual(200);
    expect(res.body.data.token).toBeDefined();
    token = res.body.data.token;
  });

  it('should allow access to protected route with token', async () => {
    const res = await request(app)
      .get('/api/auth/profile')
      .set('Authorization', `Bearer ${token}`);
    expect(res.statusCode).toEqual(200);
    expect(res.body.data.user.mobileNumber).toEqual(testUser.mobileNumber);
  });

  it('should reject unauthorized request without token', async () => {
    const res = await request(app).get('/api/auth/profile');
    expect(res.statusCode).toEqual(401);
  });
});
