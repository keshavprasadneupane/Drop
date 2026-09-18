import axios from "axios";
const rawUrl =
  import.meta.env.VITE_API_URL || "https://drop-1-5c1h.onrender.com";
const API_BASE_URL = rawUrl.replace(/\/+$/, "");

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor: attach Bearer token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("dropp_access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response interceptor: handle 401 unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if invalid or expired
      localStorage.removeItem("dropp_access_token");
      localStorage.removeItem("dropp_user");
    }
    return Promise.reject(error);
  },
);

export default api;
