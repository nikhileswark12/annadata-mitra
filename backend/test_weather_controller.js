const axios = require('axios');
require('dotenv').config();

const { getRisk } = require('./src/controllers/weatherController');

async function run() {
    process.env.PYTHON_SERVICE_URL = 'http://localhost:7000';
    
    const req = {
        body: { location: "Delhi", crop: "Wheat" },
        user: null // simulate no user to skip db save for quick test
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

    console.log("Testing with Python Service UP...");
    await getRisk(req, res, next);
}

run();
