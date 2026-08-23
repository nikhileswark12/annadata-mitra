import api from "./api";

export const getRiskAssessment = (data) => api.post("/weather/risk", data);
export const getWeatherHistory = () => api.get("/weather/history");
