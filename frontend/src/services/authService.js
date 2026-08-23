import api from "./api";

export const registerUser = async (userData) => {
  const response = await api.post("/auth/register", userData);
  if (response.data.success === true) {
    localStorage.setItem("token", response.data.data.token);
    localStorage.setItem("user", JSON.stringify(response.data.data.user));
  }
  return response.data;
};

export const loginUser = async (loginData) => {
  const response = await api.post("/auth/login", loginData);
  if (response.data.success === true) {
    localStorage.setItem("token", response.data.data.token);
    localStorage.setItem("user", JSON.stringify(response.data.data.user));
  }
  return response.data;
};

export const logoutUser = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  window.location.href = '/login';
};

export const getProfile = async () => {
  const response = await api.get("/auth/profile");
  return response.data;
};
