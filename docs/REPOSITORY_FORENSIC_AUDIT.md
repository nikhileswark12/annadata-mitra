# Annadata Mitra — Repository Forensic Audit

## 1. Repository Overview
Repository: `F:\Annadata Mitra\annadata-mitra`
Scan date: September 23, 2026

## 2. Repository Structure
- `backend/`: Node.js Express API handling routing, MongoDB connection, authentication, rate limiting, and proxying AI requests.
- `frontend/`: React application built with Vite and MUI.
- `ai-services/`: Python Flask application hosting the ML predictors and orchestrators (Vision, Crop, Market, Strategist, Weather).
- `experiments/`: Testing and experimental scripts.

## 3. Technology Stack
| Layer | Technology | Status | Evidence |
|---|---|---|---|
| Frontend | React | VERIFIED USED | `frontend/package.json` |
| Frontend | Vite | VERIFIED USED | `frontend/package.json` |
| Frontend | MUI | VERIFIED USED | `frontend/package.json` (@mui/material) |
| Frontend | Chart.js | VERIFIED USED | `frontend/package.json` |
| Frontend | i18next | NOT PRESENT | Not in `package.json` or source files |
| Backend | Node.js/Express | VERIFIED USED | `backend/package.json`, `app.js` |
| Backend | JWT | VERIFIED USED | `backend/package.json` (jsonwebtoken), `authController.js` |
| Backend | bcrypt | VERIFIED USED | `backend/package.json`, `User.js` (genSalt 12) |
| Backend | Rate Limiting | VERIFIED USED | `app.js` (express-rate-limit) |
| AI | Python/Flask | VERIFIED USED | `ai-services/requirements.txt`, `app.py` |
| AI | scikit-learn | VERIFIED USED | `ai-services/requirements.txt` |
| AI | TensorFlow/Keras | VERIFIED USED | `ai-services/requirements.txt`, `vision_service.py` |
| Database | MongoDB/Mongoose | VERIFIED USED | `backend/package.json`, `src/models/*.js` |
| External | OpenWeatherMap | VERIFIED USED | `ai-services/agents/weather_agent.py` |
| External | Gemini / Agmarknet | NOT PRESENT | Not in requirements, not in `market_service.py` or `vision_service.py` |

## 4. Backend
The backend serves as a secure gateway, providing authentication (JWT), request validation, and database operations. AI requests are proxied via Axios to the Python microservices running on `PYTHON_SERVICE_URL`.

## 5. API Endpoint Inventory
| Method | Endpoint | Implementation | Evidence |
|---|---|---|---|
| POST | `/api/auth/register` | Node.js -> MongoDB | `authRoutes.js`, `authController.js` |
| POST | `/api/auth/login` | Node.js -> MongoDB | `authRoutes.js`, `authController.js` |
| GET | `/api/auth/profile` | Node.js -> MongoDB | `authRoutes.js`, `authController.js` |
| POST | `/api/crop/recommend` | Node.js -> Python `/crop-recommend` | `cropRoutes.js`, `cropController.js` |
| POST | `/api/weather/risk` | Node.js -> Python `/weather-risk` | `weatherRoutes.js`, `weatherController.js` |
| POST | `/api/market/insights` | Node.js -> Python `/market-insights` | `marketRoutes.js`, `marketController.js` |
| POST | `/api/vision/analyze` | Node.js -> Python `/disease-detect` | `visionRoutes.js`, `visionController.js` |
| POST | `/api/strategist/generate`| Node.js -> Python `/strategist-plan`| `strategistRoutes.js`, `strategistController.js` |

## 6. Database
Mongoose Schemas:
- `User`: Handles auth, bcrypt (12 rounds).
- `CropPlan`: Logs crop recommendations. 1-year TTL (`expireAfterSeconds: 31536000`).
- `WeatherLog`: Logs weather history. 30-day TTL (`expireAfterSeconds: 2592000`).
- `Strategy`: Logs strategist output.
- `MarketSearch`: Logs market queries.
- `DiseaseQuery`: Logs vision queries.

Schemas like `farms`, `crops`, `recommendations`, `cropImages`, or `marketPrices` are not defined.

## 7. Crop Planning Agent
- **Implementation:** `ai-services/services/crop_service.py`
- Loads `crop_model.pkl` and `crop_scaler.pkl` using joblib.
- Inputs are scaled, and probabilities generated via `predict_proba`.
- Logic mapped through `CropReasoner`.

## 8. Climate & Risk Agent
- **Implementation:** `ai-services/agents/weather_agent.py`
- Uses OpenWeatherMap API if `OPENWEATHER_API_KEY` is provided, else generates synthetic deterministic weather based on location hash.
- Fetches current weather conditions (no 5-day forecast endpoints used).
- Implements a 10-minute (600s) in-memory cache dictionary `_CACHE` to limit API usage.
- Does NOT use `node-cron` or scheduled nightly tasks.

## 9. Vision Agronomist Agent
- **Implementation:** `ai-services/services/vision_service.py`
- Uses `tf.keras.models.load_model('vision_model.h5')`.
- Resizes images to 224x224 and predicts leaf disease.
- Architecture is LOCAL ONLY. No Gemini API, Google Generative AI, or cloud inference fallback present in the code.
- No dynamic Laplacian blur detection implementation found.

## 10. Market Intelligence Agent
- **Implementation:** `ai-services/services/market_service.py`
- Uses a static CSV dataset loaded via `pd.read_csv('mandi_prices.csv')`.
- No live scraping from Agmarknet via BeautifulSoup.
- No ARIMA or Linear Regression models implemented; relies on static CSV data for rule-based pricing and synthetic fallback insights.

## 11. Strategist Agent
- **Implementation:** `ai-services/services/strategist_service.py`
- Implemented as a Python Flask route `/strategist-plan` which orchestrates inputs.
- Orchestration executes sequentially across other local predictors via `registry.get()`.
- Does NOT use Node.js `Promise.all()` for parallel invocation.

## 12. Frontend
- Built with React + Vite + MUI + Chart.js.
- **Languages:** Multi-language (i18n) support is NOT PRESENT in the codebase (no i18next installed or implemented).

## 13. Datasets
- Found datasets in `ai-services/datasets/mandi/`:
  - `mandi_prices.csv`, `processed_prices.csv`, `train.csv`, `test.csv`, `val.csv`

## 14. ML Models
- `vision_model.h5` and `class_names.json` expected by `vision_service.py`.
- `crop_model.pkl` and `crop_scaler.pkl` expected by `crop_service.py`.
- No ARIMA models or other explicit serialized files.

## 15. Security
- **bcrypt salt rounds:** 12 (`User.js`).
- **JWT expiration:** Default '7d' (configurable via `.env`).
- **Rate limiting:** 20/15min for auth, 200/15min for general API routes.
- Helmet, express-mongo-sanitize, CORS all implemented.

## 16. Caching
- **CropPlan MongoDB TTL:** 1 year (365 days).
- **WeatherLog MongoDB TTL:** 30 days.
- **Weather Service:** 10-minute in-memory Python dictionary cache.

## 17. Testing
- **VERIFIED TESTS:** Jest test files (`auth.test.js`, `api.test.js`, `utils.test.js`, `middleware.test.js`, `aiServices.test.js`) with explicit assertions (`expect`) found in `backend/tests`.

## 18. CI/CD and Deployment
- **NOT PRESENT:** No `.github/workflows`, `Dockerfile`, `docker-compose.yml`, or other CI/CD orchestration files found.

## 19. Languages
- **PLANNED/DOCUMENTED ONLY:** Codebase is fundamentally monolingual (English). No actual translation logic implemented.

## 20. External APIs
- **VERIFIED:** OpenWeatherMap (via Python `urllib` in `weather_agent.py`).
- **NOT PRESENT:** Gemini Vision API, Agmarknet scraping, external forecasting services.

## 21. Implementation Status
| Feature | Status |
|---|---|
| Crop Planning (ML) | VERIFIED IMPLEMENTED |
| Weather & Climate (API/Synthetic) | VERIFIED IMPLEMENTED |
| Vision Disease Detect (Local CNN) | VERIFIED IMPLEMENTED |
| Market Intelligence (Static CSV) | VERIFIED IMPLEMENTED |
| Market Intelligence (Agmarknet) | NOT PRESENT |
| Vision Agent (Gemini API) | NOT PRESENT |
| Security (JWT, bcrypt, rate limit) | VERIFIED IMPLEMENTED |
| Multilingual Support | NOT PRESENT |
| CI/CD & Cloud Deployment | NOT PRESENT |

## 22. Documentation vs Code Contradictions
1. **Strategist Execution:** Documented as Node.js `Promise.all()` parallel execution; code is sequential Python registry execution.
2. **Vision Model:** Documented as dual-path with Gemini fallback; code is strictly local Keras/MobileNetV2.
3. **Market Sourcing:** Documented as nightly Agmarknet scraping; code uses a static local CSV.
4. **Market Modeling:** Documented as ARIMA/Linear Regression; code is rule-based evaluation.
5. **Weather Forecasting:** Documented as 5-day predictive; code pulls current weather only.
6. **Weather Caching:** Documented as nightly `node-cron` fetching; code uses a 10-minute on-demand in-memory cache and 30-day DB TTL.
7. **Crop TTL:** Documented as 24-hour cache; code implements 1-year DB TTL.
8. **I18n:** Documented as multilingual; code contains no translation mechanism.

## 23. Unsupported Claims Found in Documentation
- Agmarknet scraping via BeautifulSoup.
- Gemini Vision API usage.
- `Promise.all` orchestration in Node.js.
- ARIMA forecasting.
- CI/CD workflows and Dockerized cloud deployment.
- Multilingual i18next support.

## 24. Important Evidence Files
- `ai-services/services/vision_service.py`: Confirms local Keras CNN, no Gemini.
- `ai-services/services/market_service.py`: Confirms CSV loading (`pd.read_csv`), no scraping or ARIMA.
- `ai-services/services/strategist_service.py`: Confirms sequential Python-based execution.
- `ai-services/agents/weather_agent.py`: Confirms 10-min in-memory cache and current OWM data, synthetic fallback.
- `backend/src/models/CropPlan.js`: Confirms 1-year TTL.
- `backend/src/models/User.js`: Confirms bcrypt 12 salt rounds.

============================================================
FINAL SUMMARY
============================================================

REPOSITORY SCAN COMPLETED

Repository:
    `F:\Annadata Mitra\annadata-mitra`

Major verified components:
    React Frontend, Node.js/Express Backend API, MongoDB Models, Python Flask AI Services (Vision CNN, CSV-based Market agent, ML-based Crop agent, OWM-based Weather agent).

Major implementation findings:
    The system is a fully functioning local prototype operating fundamentally through a Node.js Express backend and a Python Flask ML microservice layer. It heavily relies on static datasets (Market), local pre-trained ML models (Vision, Crop), and simple heuristic rule evaluation (Strategist, Market).

Major contradictions:
    Significant contradictions exist between theoretical design (Cloud deployment, Gemini Vision, Agmarknet live scraping, ARIMA forecasting, node-cron tasks, Node.js `Promise.all`) and the actual, purely local, deterministic prototype implementation.

Features documented but not implemented:
    - Agmarknet BeautifulSoup Scraper
    - Gemini Cloud Vision path
    - ARIMA/Linear Regression logic
    - 5-day predictive weather forecasting
    - CI/CD & Docker orchestration
    - Multilingual i18n support

REPORT WAS NOT MODIFIED:
    YES

PROJECT REPOSITORY WAS NOT MODIFIED:
    YES
