/// <reference types="vitest" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      // Proxy /search requests to backend
      "/api/search": {
        target: "http://127.0.0.1:8080",
        changeOrigin: true,
        secure: false
      }
    }
  },
  test: {
    globals: true,
    environment: "happy-dom",
    setupFiles: ["./tests/vitest.setup.ts"],
    include: ["tests/**/*.{test,spec}.{ts,tsx}"],
    css: false
  },
  optimizeDeps: {
    include: [
      "react",
      "react-dom",
      "antd",
      "@ant-design/icons",
      "@testing-library/react"
    ]
  }
});
