import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

// Request interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle global errors and unauthorized states
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Handle 401 Unauthorized globally
      if (error.response.status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        // Only redirect if not already on login/register pages
        if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
          window.location.href = '/login';
        }
      }
      
      // Standardize error format for the frontend
      const message = error.response.data?.error || error.response.data?.message || "An unexpected error occurred.";
      const details = error.response.data?.details || error.response.data?.errors || null;
      return Promise.reject({ message, details, status: error.response.status });
    } else if (error.request) {
      return Promise.reject({ message: "Network error. Please check your connection.", status: 0 });
    } else {
      return Promise.reject({ message: error.message, status: 500 });
    }
  }
);

export default api;
