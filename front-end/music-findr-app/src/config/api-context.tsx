import { createContext, useContext } from "react";
import type { AxiosInstance } from "axios";

export interface ApiContextProps {
  apiClient: AxiosInstance;
}

export const ApiContext = createContext<ApiContextProps | undefined>(undefined);

export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error("useApi must be used within an ApiProvider");
  }
  return context;
};
