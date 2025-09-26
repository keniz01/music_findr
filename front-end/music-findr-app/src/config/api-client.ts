import axios, { type InternalAxiosRequestConfig } from "axios";

const ApiClient = axios.create({
  baseURL: "",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor
ApiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    config.maxRedirects = 0;
    config.headers["Pragma"] = "no-cache";
    console.log("[API Request]", config);
    return config;
  },
  (error: Error) => {
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
  (error: Error) => {
    console.error("[API Response Error]", error);
    return Promise.reject(error);
  },
);

export default ApiClient;
