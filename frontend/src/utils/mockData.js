export const cropResults = [
  { crop: "Rice", score: 92 },
  { crop: "Maize", score: 84 },
  { crop: "Cotton", score: 76 },
];

export const weatherData = {
  temperature: "31°C",
  humidity: "68%",
  condition: "Partly Cloudy",
};

export const forecastData = [
  { day: "Mon", temp: "31°C" },
  { day: "Tue", temp: "30°C" },
  { day: "Wed", temp: "29°C" },
  { day: "Thu", temp: "32°C" },
  { day: "Fri", temp: "33°C" },
];

export const riskAlerts = [
  { severity: "HIGH", message: "Heavy rainfall expected during flowering stage." },
  { severity: "MEDIUM", message: "Pest risk may increase due to humidity rise." },
];

export const diseaseMockResult = {
  status: "Infected",
  disease: "Leaf Blight",
  confidence: 94,
  severity: "High",
  treatment: [
    "Remove severely affected leaves immediately.",
    "Spray recommended fungicide as per dosage guidelines.",
    "Avoid overhead irrigation for the next few days.",
    "Monitor nearby plants for similar symptoms.",
  ],
};

export const marketMockData = {
  recommendation: {
    market: "Vadodara Mandi",
    crop: "Rice",
    expectedPrice: 2450,
    trend: "Rising",
    reason: "Higher demand and better average selling price in the selected region.",
  },
  prices: [
    { market: "Vadodara Mandi", crop: "Rice", price: 2450, distance: "12 km" },
    { market: "Anand Market Yard", crop: "Rice", price: 2380, distance: "28 km" },
    { market: "Ahmedabad APMC", crop: "Rice", price: 2510, distance: "65 km" },
    { market: "Nadiad Market", crop: "Rice", price: 2410, distance: "34 km" },
  ],
  trends: [
    { day: "Mon", price: 2280 },
    { day: "Tue", price: 2320 },
    { day: "Wed", price: 2360 },
    { day: "Thu", price: 2400 },
    { day: "Fri", price: 2450 },
  ],
};

export const strategistMockData = {
  priorities: [
    {
      title: "Apply fungicide immediately",
      level: "High",
      description: "Disease severity is high and delay may spread infection to nearby plants.",
    },
    {
      title: "Delay irrigation for 2 days",
      level: "Medium",
      description: "Current humidity and disease conditions make excess moisture risky.",
    },
    {
      title: "Monitor mandi prices daily",
      level: "Low",
      description: "Price trend is rising, so waiting may improve selling opportunity.",
    },
  ],
  timeline: [
    {
      phase: "Immediate",
      actions: [
        "Remove visibly infected leaves.",
        "Spray recommended fungicide in affected areas.",
        "Avoid overhead watering.",
      ],
    },
    {
      phase: "This Week",
      actions: [
        "Track disease spread across nearby crop rows.",
        "Review 5-day weather forecast before irrigation.",
        "Record crop condition updates in the dashboard.",
      ],
    },
    {
      phase: "This Month",
      actions: [
        "Compare market prices across nearby mandis.",
        "Adjust crop management based on recurring risk alerts.",
      ],
    },
  ],
  conflictResolution: {
    issue: "Weather suggests irrigation soon, but disease risk suggests reducing leaf moisture.",
    resolution:
      "Use controlled root-zone irrigation instead of overhead irrigation. This balances plant water needs while reducing disease spread risk.",
  },
};