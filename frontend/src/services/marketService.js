
import api from "./api";

export const getMarketInsights = async (data) => {
  const response = await api.post("/market/insights", data);
  return response;
};

export const getMarketHistory = () => api.get("/market/history");
