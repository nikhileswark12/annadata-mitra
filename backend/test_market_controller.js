const axios = require('axios');
require('dotenv').config();

const { getInsights } = require('./src/controllers/marketController');

async function run() {
    process.env.PYTHON_SERVICE_URL = 'http://localhost:7000';
    
    const req = {
        body: { crop: "Wheat", location: "Delhi", quantity: 100 },
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
    await getInsights(req, res, next);
    process.exit(0);
}

run();
