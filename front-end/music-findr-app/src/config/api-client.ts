// src/api/ApiClient.ts
import axios from "axios";

const ApiClient = axios.create({
  baseURL: "https://api.example.com", // Replace with your actual API base URL
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
ApiClient.interceptors.request.use(
  (config) => {
    console.log("[API Request]", config);
    return config;
  },
  (error) => {
    console.error("[API Request Error]", error);
    return Promise.reject(error);
  },
);

// Response interceptor
ApiClient.interceptors.response.use(
  (response) => {
    console.log("[API Response]", response);
    return response;
  },
  (error) => {
    console.error("[API Response Error]", error);
    return Promise.reject(error);
  },
);

export default ApiClient;
