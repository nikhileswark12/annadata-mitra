import api from "./api";

export const getCropRecommendation = (data) =>
  api.post("/crop/recommend", data);

export const getCropHistory = () =>
  api.get("/crop/history");
