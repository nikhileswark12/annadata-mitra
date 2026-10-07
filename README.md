<div align="center">
  <h1>Annadata Mitra</h1>
  <p><b>AI-Powered Agricultural Decision Support System for Indian Farmers</b></p>
</div>

Annadata Mitra is a farmer-centric agricultural decision-support platform designed to support the farming lifecycle—from pre-sowing crop planning through crop-health assessment, climate-risk analysis, market intelligence, and strategic synthesis.

The current implementation combines machine-learning inference, deterministic reasoning agents, and a Strategist orchestration layer. Outputs are designed to be explainable and source-aware; the system does not claim live or predictive data when the configured data source is unavailable.

---

## About the Project

Indian agriculture faces multifaceted challenges that heavily impact farmer livelihoods. Annadata Mitra was developed to address these core problems:
* **Uncertain weather and climate conditions**
* **Inefficient crop selection**
* **Delayed crop disease detection**
* **Limited access to reliable mandi prices**
* **Distress selling and poor market timing**
* **Lack of centralized agricultural decision support**
* **Language and accessibility barriers**

Unlike monolithic LLM wrappers, Annadata Mitra is designed as a **multi-agent agricultural decision-support architecture**. It combines machine learning, computer vision, weather intelligence, market intelligence, and deterministic decision synthesis into a single, unified, offline-capable platform.

## Key Features

* **AI-based crop recommendation**
* **Soil and climate-aware crop planning**
* **Weather-risk analysis with live OpenWeatherMap support when configured, plus an explicitly labelled synthetic seasonal fallback**
* **Agricultural climate-risk assessment**
* **Extreme-weather alerts**
* **Plant disease and crop-health analysis**
* **Image-based crop disease detection**
* **MobileNetV2-based vision architecture**
* **Mandi price intelligence**
* **Short-term market guidance from the available mandi dataset and rule-based reasoning**
* **Multi-mandi comparison**
* **Farmer-specific decision support**
* **Multi-agent decision synthesis**
* **Priority-based agricultural action plans**
* **Conflict resolution between recommendations**
* **Multilingual interface** (Hindi, Marathi, English)
* **Responsive farmer-facing dashboard**
* **Secure authentication and protected APIs**

*(Note: Advanced features like direct Edge NLP and Gemini Vision fallbacks are part of the documented future scope rather than the current v1.0.0 implementation).*

## Agricultural Lifecycle

The system architecture is designed directly around the complete agricultural lifecycle:

```text
Pre-Sowing
    ↓
Crop Planning
    ↓
Crop Monitoring
    ↓
Disease / Health Assessment
    ↓
Harvest Planning
    ↓
Market Intelligence
    ↓
Strategic Decision Support
```

## AI Agents

Annadata Mitra utilizes a specialized five-agent architecture.

### Agent 1 — Crop Planning Agent
* Evaluates soil NPK, pH, temperature, humidity, and rainfall inputs.
* Utilizes a **Random Forest classification** model.
* Provides crop suitability prediction and top crop recommendations.
* Deployed as a Python/scikit-learn inference pipeline within a Flask microservice via `joblib` serialization.

### Agent 2 — Climate & Risk Agent
* Uses **OpenWeatherMap** when `OPENWEATHER_API_KEY` is configured.
* Falls back to deterministic synthetic seasonal weather when a live key is unavailable or the live request fails; the response explicitly identifies this source.
* Applies agricultural risk rules and generates preventive recommendations.
* Uses a short-lived in-memory cache.

### Agent 3 — Vision Agronomist Agent
* Dedicated to visual pathology diagnosis.
* Operates primarily on a **MobileNetV2 CNN** custom trained on PlantVillage.
* Implements the following dual-path architecture:

```text
Crop Image
    ↓
Image Validation
    ↓
Image Quality Assessment
    ↓
Preprocessing
    ↓
Connectivity Check
    ├── Online → Gemini Vision (Documented Fallback)
    └── Offline → MobileNetV2 CNN (Primary Implementation)
    ↓
Disease / Health Result
    ↓
Confidence Assessment
    ↓
Treatment Recommendation
```

### Agent 4 — Market Intelligence Agent
* Uses the repository's mandi-price dataset for available crops.
* Implements multi-mandi comparison and rule-based market reasoning.
* Generates selling recommendations when source data is available.
* Does **not** silently substitute synthetic market prices when the requested crop or dataset is unavailable.
* The frontend's short-term projection is an interpolation between current and predicted values; it is not a day-by-day historical series.

### Agent 5 — Strategist Agent
The core decision-synthesis layer. It invokes the available leaf agents through a deterministic orchestration flow and applies a strict priority hierarchy:

```text
Safety > Health > Timing > Economics
```

* Orchestrates the Crop, Weather, and Market agents and records whether each source is available, insufficient, or failed.
* Performs **Conflict detection** and **Conflict resolution** (e.g., stopping pesticide application during heavy rainfall).
* Generates timeline-based action grouping.
* Provides unified, farmer-friendly guidance in multilingual outputs.

## System Architecture

```text
                    Farmer
                       │
                       ▼
              React Web Interface
                       │
                 REST / Axios
                       │
                       ▼
             Node.js / Express API
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
        MongoDB            AI Orchestrator
                                 │
          ┌──────────────────────┼──────────────────────┐
          │          │           │           │           │
          ▼          ▼           ▼           ▼           ▼
       Crop       Climate      Vision      Market    Strategist
       Agent      & Risk       Agent       Agent       Agent
          │          │           │           │
          ▼          ▼           ▼           ▼
      Flask / ML   Weather     CNN /      Agmarknet
      Service       API       Vision API    / ML
```

## Technology Stack

| Category | Technologies |
| :--- | :--- |
| **Languages** | JavaScript, Python |
| **Frontend** | React.js, Vite, Material UI, Chart.js, Axios, i18next |
| **Backend** | Node.js, Express.js, JWT, Multer, bcrypt |
| **AI / ML** | Python, scikit-learn, TensorFlow/Keras, OpenCV, Pillow, pandas, NumPy, joblib |
| **Database** | MongoDB, Mongoose |
| **AI Services** | Flask |
| **External Data** | OpenWeatherMap, Agmarknet, data.gov.in |
| **Vision** | MobileNetV2 |
| **Dev Tools** | Git, GitHub, VS Code, Postman |

*(Docker deployment pipelines are documented for future release integration).*

## Architecture Layers

* **Presentation Layer:** React.js, MUI, forms, charts, dashboard, and multilingual interface.
* **API Gateway Layer:** Node.js and Express.js handling authentication, validation, routing, file uploads, and agent orchestration.
* **Intelligence Layer:** Python Flask microservices executing the agricultural AI agents and inference pipelines.
* **Data Layer:** MongoDB/Mongoose handling farmer profiles, farms, crops, recommendations, crop images, market prices, and the weather cache.
* **External Services:** APIs for meteorological and agricultural market data.

## Project Structure

```text
annadata-mitra/
├── frontend/                            # React.js web application
├── backend/                             # Node.js API Gateway & MongoDB models
├── ai-services/                         # Python Flask server & AI logic
│   ├── datasets/                        # Canonical, hashed datasets
│   ├── models/                          # Frozen ML weights (.keras, .pkl)
│   ├── experiments/                     # Verified E1-E7 JSON metrics and assets
│   └── scratch/                         # Automated validation scripts
├── reviewer_reproducibility_bundle/     # Hash manifests and provenance matrices
├── submission_package/                  # Conference submission assets
├── package.json
├── README.md
└── CITATION.cff                         
```

## API Modules

**Current implemented endpoints:**

```text
# Authentication
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/profile

# Crop Planning
POST /api/crop/recommend
GET  /api/crop/history

# Climate & Risk
POST /api/weather/risk
GET  /api/weather/history

# Vision Agronomist
POST /api/vision/analyze
GET  /api/vision/history

# Market Intelligence
POST /api/market/insights
GET  /api/market/history

# Decision Synthesis
POST /api/strategist/generate
GET  /api/strategist/history

# Dashboard
GET  /api/dashboard/stats
```

All agent and dashboard endpoints require JWT authorization through the Node.js API Gateway.

## Data & Datasets

The repository relies on several verified, canonical datasets strictly tracked for reproducibility:
* **Crop Recommendation Dataset:** Synthetic/Tabular NPK datasets utilized for training the Random Forest model.
* **PlantVillage:** The foundational image dataset utilized for MobileNetV2 pathology training.
* **Agmarknet & data.gov.in:** Market intelligence pricing data sources.
* **OpenWeatherMap & IMDAA:** Meteorological risk thresholds and analysis data.

## Machine Learning Pipeline

```text
Dataset
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Train / Validation Split
   ↓
Model Training
   ↓
Evaluation
   ↓
Model Serialization (.pkl / .keras)
   ↓
Flask Inference Service
   ↓
Node.js API
   ↓
React Dashboard
```
* **Crop Recommendation Pipeline:** Preprocessed tabular NPK and environmental data trained on a Scikit-Learn Random Forest Classifier.
* **Vision Pipeline:** Standardized 224x224 RGB image tensors evaluated through a fine-tuned MobileNetV2 architecture with GlobalAveragePooling2D.

## Security

* **Authentication:** Secure stateless JWT authentication.
* **Passwords:** `bcrypt` salted password hashing.
* **Validation:** Strict Express middleware input validation and sanitized file uploads via `Multer`.
* **Rate Limiting:** Protects the Node.js gateway from DDOS attacks.
* **Configuration:** 100% environment-variable based secrets mapping.

## Environment Variables

Copy the `.env.example` in `backend/` and `ai-services/` to a local `.env` and populate.

```env
# Example configuration
MONGO_URI=mongodb://localhost:27017/annadata_mitra
JWT_SECRET=your_secure_jwt_secret_here
PORT=5000
PYTHON_SERVICE_URL=http://localhost:7000
OPENWEATHER_API_KEY=your_openweathermap_api_key
USE_MOCK_MODELS=false
```

## Installation

```bash
# Clone the repository
git clone https://github.com/nikhileswark12/annadata-mitra.git
cd annadata-mitra

# 1. Backend Setup
cd backend
npm install

# 2. Frontend Setup
cd ../frontend
npm install

# 3. AI Services Setup
cd ../ai-services
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Project

For local development, initiate the stack in the following order:

```bash
# 1. Ensure MongoDB is running locally or via cloud
mongod

# 2. Start AI Services (Port 7000)
cd ai-services
python app.py

# 3. Start Backend API Gateway (Port 5000)
cd backend
npm run dev

# 4. Start React Frontend (Port 5173 or 3000)
cd frontend
npm run dev
```

## Testing

The repository defines build/lint/test commands for the individual application layers. A complete live end-to-end run still requires the local MongoDB, Node backend, AI service, model/data artifacts, and frontend to be started together.

```bash
# Frontend
cd frontend
npm run build
npm run lint

# Backend
cd backend
npm test

# AI service
cd ai-services
pytest
```

These commands should be treated as layer-level verification unless a complete environment is available. No claim of successful live E2E execution is made solely from the repository source.

## Development Methodology

The project was executed through a rigorous phased development and scientific validation approach:
1. Foundation / repository stabilization
2. Codebase standardization
3. AI architecture standardization
4. Knowledge & Reasoning engine architecture
5. System integration and verification
6. Agent implementation
7. Testing and final validation (Phases 6.7 through 8.6)

## Current Project Status

The repository contains the five-agent application architecture and the integrated frontend/backend/AI-service flow. Validation results should be interpreted according to the current implementation and the configured data/model sources; synthetic weather fallback and unavailable market data are explicitly surfaced rather than treated as live data.

```text
Crop Planning       ██████████ (Verified - 99.09% Acc)
Climate & Risk      ██████████ (Verified - Rules Engine)
Vision              ██████████ (Verified - 88.71% Top-1)
Market Intelligence ███████░░░ (Partially Implemented - Heuristics)
Strategist          ██████████ (Verified - 100% Conflict Safety)
Integration         █████████░ (Contract verified; live E2E environment required)
Testing             ███████░░░ (Layer-level commands defined; live E2E evidence environment-dependent)
```

## Limitations

* **External Dependencies:** Reliance on OpenWeatherMap and Agmarknet for real-time temporal data.
* **Heuristic Limitations:** Market intelligence currently relies on rule-based heuristics rather than predictive LSTMs due to historical dataset constraints.
* **Domain Gap:** Laboratory-to-field domain gap persists for PlantVillage-trained CNNs evaluating real-world field images.
* **Connectivity:** Baseline dependency on local server synchronization for heavy image processing tasks.

## Future Scope

* Integration of satellite and drone imagery.
* IoT sensor integration for precise field-level NPK/moisture readings.
* Offline/Edge AI processing directly on mobile hardware.
* Voice-based multilingual interaction and expanded regional language support (NLP).
* Direct buyer/logistics integration and crop insurance advisory.

## Project Documentation

Detailed academic and architectural documents can be referenced directly:
* `Annadata_Mitra_Complete_System_Specification.docx`
* `Annadata_Mitra_Complete_Flowcharts.docx`
* `Annadata_Mitra_Literature_Review.docx`
* `Annadata_Mitra_Report.pdf`
* `ANNADATA_MITRA_FINAL_COMPLETION_REPORT.md` (Execution summary)

## Academic Information

Developed as a B.Tech Computer Science & Engineering research project.