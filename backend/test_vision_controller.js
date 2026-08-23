const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const { analyze } = require('./src/controllers/visionController');

async function run() {
    process.env.PYTHON_SERVICE_URL = 'http://localhost:7000';
    
    // Create a dummy image for testing
    const testImgPath = path.join(__dirname, 'test_img.jpg');
    fs.writeFileSync(testImgPath, 'dummy image content');

    const req = {
        file: {
            filename: 'test_img.jpg',
            path: testImgPath,
            mimetype: 'image/jpeg'
        },
        user: null // simulate no user to skip db save
    };
    
    const res = {
        status: function(s) {
            this.statusCode = s;
            return this;
        },
        json: function(d) {
            console.log("Status:", this.statusCode);
            console.log("JSON:", JSON.stringify(d, null, 2));
        }
    };
    
    const next = (err) => console.error("Next called with:", err);

    console.log("Testing with Python Service...");
    await analyze(req, res, next);
    
    // cleanup
    fs.unlinkSync(testImgPath);
    process.exit(0);
}

run();
