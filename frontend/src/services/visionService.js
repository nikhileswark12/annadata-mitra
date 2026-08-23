import api from "./api";

export const analyzeCropImage = (formData) =>
  api.post("/vision/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
    timeout: 60000,
  });

export const getVisionHistory = () => api.get("/vision/history");
