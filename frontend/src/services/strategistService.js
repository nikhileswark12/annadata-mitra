import api from "./api";

export const getUnifiedGuidance = (data) => api.post("/strategist/generate", data);
export const getStrategistHistory = () => api.get("/strategist/history");
