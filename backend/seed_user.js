const mongoose = require('mongoose');
const User = require('./src/models/User');

mongoose.connect('mongodb://localhost:27017/annadata_mitra').then(async () => {
    const user = new User({
        fullName: 'Test User',
        mobileNumber: '1234567890',
        email: 'test@example.com',
        password: 'password123'
    });
    try {
        await user.save();
        console.log('User created');
    } catch(e) {
        console.log('User might already exist or error', e.message);
    }
    mongoose.disconnect();
});
