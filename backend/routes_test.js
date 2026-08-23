
process.env.MONGO_URI='mongodb://localhost:27017/test'; process.env.JWT_SECRET='test';
process.env.PYTHON_SERVICE_URL='http://localhost:7000'; process.env.FRONTEND_URL='http://localhost:5173';
process.env.NODE_ENV='development'; process.env.PORT='5000';
try {
  const app = require('./src/app');
  app._router.stack.filter(r => r.name === 'router').forEach(r => r.handle.stack.filter(s => s.route).forEach(s => console.log(Object.keys(s.route.methods)[0].toUpperCase(), s.route.path)));
} catch(e) { console.log('CRASH:', e.message); }
