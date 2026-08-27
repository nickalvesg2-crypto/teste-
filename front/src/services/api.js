import axios from "axios";

const api = axios.create({
  // Mantenha APENAS a URL base do backend aqui
  baseURL: import.meta.env.VITE_API_URL || "https://teste-3x8p.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;