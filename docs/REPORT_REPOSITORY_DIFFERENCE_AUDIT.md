# Annadata Mitra — Report vs Repository Difference Audit

## 1. Audit Scope
This audit compares the claims in the `main.pdf` and its constituent `.tex` files for the Annadata Mitra Project-II against the current verified repository codebase (`F:\Annadata Mitra\annadata-mitra`).

## 2. Source-of-Truth Rules
The repository codebase acts as the definitive source of truth. Any claim made in the report that cannot be corroborated by the current codebase is treated as unsupported or a mismatch.

## 3. Executive Summary
The report has undergone significant updates to correct major discrepancies (such as Gemini Vision, Agmarknet, and Promise.all) but still contains residual contradictions. Key areas requiring adjustment include dataset schemas, caching TTLs, predictive weather claims, and i18next multilingual support.

## 4. Verified Report Claims
- React, Vite, MUI, Chart.js usage for the frontend.
- Node.js, Express, MongoDB usage for the backend.
- Python Flask usage for the AI agents layer.
- Random Forest model usage for Crop Planning.
- Keras/MobileNetV2 model usage for Vision Agent.
- Static CSV dataset usage for Market Intelligence.
- OpenWeatherMap API usage for Weather conditions.
- JWT and bcrypt (12 salt rounds) security implementations.
- Rate limiting configurations (20/15min auth, 200/15min API).
- API Endpoints accurately reflect actual routes.
- Project-II, 7th Semester, Academic Year 2026-2027 academic metadata.

## 5. Mismatched Claims

| # | Report Location | Report Claim | Repository Reality | Classification | Evidence |
|---|---|---|---|---|---|
| 1 | Chapter 3, Sec 4.2 | 5-day forecasts based on GPS | Only fetches current weather data | MISMATCH | `weather_agent.py` |
| 2 | Chapter 3, Sec 5.1 | 24-hour TTL for crop recommendations | TTL is 1 year (365 days) | MISMATCH | `CropPlan.js` schema TTL |
| 3 | Chapter 3, Sec 5.1 | 6-hour TTL for weather data | 30-day DB TTL, 10-minute in-memory cache | MISMATCH | `WeatherLog.js` |
| 4 | Chapter 4, Sec 1.5 | Database contains collections for farms, crops, recommendations, crop images, market prices, and weather caches. | Collections are: users, CropPlan, WeatherLog, Strategy, MarketSearch, DiseaseQuery. | MISMATCH | `backend/src/models/` |
| 5 | Chapter 4, Sec 2 | 7-day weather forecasts | Only fetches current weather data | MISMATCH | `weather_agent.py` |
| 6 | Chapter 4, Sec 2 | 30-day historical trends, 7-day ML forecasts | Market service returns synthetic trend logic, no ML forecast or historical API. | MISMATCH | `market_service.py` |
| 7 | Chapter 6, Sec 4 | Mongoose schemas mapped for farms, crops, recommendations, cropImages, marketPrices | These models do not exist in the backend. | MISMATCH | `backend/src/models/` |

## 6. Unsupported Claims

| # | Report Location | Unsupported Claim | Evidence Check | Classification |
|---|---|---|---|---|
| 1 | Abstract | "The platform features a multilingual... interface" | No i18next or translation files exist in the frontend | UNSUPPORTED |
| 2 | Chapter 6, Sec 2 | i18next Multilingual support (English, Hindi, Gujarati) | No i18next in `package.json` | UNSUPPORTED |
| 3 | Chapter 6, Sec 3.5 | Final decision logic is translated... using i18next | No translation implementation in frontend or backend | UNSUPPORTED |
| 4 | Chapter 6, Sec 4 | User schema contains `language` field | `User.js` does not have `language` | UNSUPPORTED |

## 7. Outdated Claims
- The claim of "caching mechanisms (e.g., 24-hour TTL... 6-hour TTL)" represents an outdated system constraint.

## 8. Chapter-by-Chapter Findings
- **Chapter 1:** Correct content.
- **Chapter 2:** Correct content. (ARIMA mentioned in literature review, which is valid context).
- **Chapter 3:** Needs corrections for 5-day weather, 24-hour crop TTL, and 6-hour weather TTL.
- **Chapter 4:** Needs corrections for DB collections, 7-day weather forecasts, and 7-day ML market forecasts.
- **Chapter 5:** Correct content.
- **Chapter 6:** Needs corrections for i18next, missing DB schemas, and translation claims.
- **Chapter 7 & 8:** Correct content.
- **Chapter 9:** Plagiarism/Survey content. No modifications required.

## 9. API Differences
- The documented API endpoints match the repository routing precisely.

## 10. Database Differences
- The report claims schemas for `farms`, `crops`, `cropImages`, and `marketPrices`. These do not exist in the repository.
- The actual schemas are `User`, `CropPlan`, `WeatherLog`, `Strategy`, `MarketSearch`, `DiseaseQuery`.
- The `User` schema documented in Chapter 6 includes fields (`language`) not present in the code.

## 11. AI Agent Differences
- **Crop Planning:** TTL is 1 year, not 24 hours.
- **Climate & Risk:** Fetches current conditions, not 5/7-day forecasts.
- **Market Intelligence:** Uses static CSV. Does not provide 30-day historical/7-day ML forecasts.
- **Vision:** Local Keras MobileNetV2. Matches code.
- **Strategist:** Sequential Python registry. Matches code.

## 12. Security Differences
- bcrypt 12 rounds, JWT, rate limiting are all accurately described in the report.

## 13. Frontend Differences
- i18next multilingual support is entirely missing from the frontend implementation, contradicting Abstract and Chapter 6 claims.

## 14. Dataset / Model Differences
- Models and datasets referenced in the updated report generally align with `vision_model.h5`, `crop_model.pkl`, and `mandi_prices.csv`.

## 15. Testing Differences
- The backend contains verified unit tests (Jest) with explicit assertions, validating report claims of functional testing.

## 16. Deployment / CI-CD Differences
- The report makes no explicit, unsupported claims of Docker or CI/CD pipelines in its current state.

## 17. Diagram / Flowchart Corrections
- **Figure 4.2 (User Interaction Flow):** Text references 7-day forecasts which are not implemented.

## 18. Academic Information Check
- Project-II, 7th Semester, Academic Year 2026–2027, Course Code: 303105423, November 2026. All verified and correct.

## 19. Required Report Changes

**A. MUST CHANGE**
- Remove or correct 5-day and 7-day weather forecast claims in Chapters 3 & 4.
- Remove or correct 7-day ML and 30-day historical market forecast claims in Chapter 4.
- Update MongoDB schemas in Chapter 4 & 6 to match actual Mongoose models.
- Correct the TTL metrics in Chapter 3 (24h -> 1 year; 6h -> 10m/30d).
- Remove i18next multilingual claims from Abstract and Chapter 6.

**B. SHOULD CHANGE**
- Refine wording regarding "continuous monitoring" to reflect on-demand agent invocation.

**C. OPTIONAL CLARIFICATION**
- N/A

**D. DO NOT CHANGE**
- Academic metadata, Chapter 9, Security metrics, verified agent architectures.

## 20. Final Consistency Checklist
- [x] Codebase vs Documented Endpoints
- [x] Codebase vs Documented Models
- [x] Codebase vs Documented Caching
- [x] Codebase vs Documented AI Pathing
