import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

const config: Config = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            color: "#333",
            a: { color: "#3b82f6", textDecoration: "none" },
            strong: { fontWeight: "600" }
          }
        }
      }
    }
  },
  plugins: [typography]
};

export default config;
