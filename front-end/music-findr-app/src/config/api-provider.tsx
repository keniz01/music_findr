import type { AxiosInstance } from "axios";
import { createContext, useContext, useMemo, type ReactNode } from "react";
import ApiClient from "./api-client";

interface ApiContextProps {
  apiClient: AxiosInstance;
}

const ApiContext = createContext<ApiContextProps | undefined>(undefined);

export const useApi = () => {
  const context = useContext(ApiContext);
  if (!context) {
    throw new Error("useApi must be used within an ApiProvider");
  }
  return context;
};

interface ApiProviderProps {
  children: ReactNode;
}

export const ApiProvider: React.FC<ApiProviderProps> = ({ children }) => {
  const contextValue = useMemo(() => ({ apiClient: ApiClient }), []);

  return (
    <ApiContext.Provider value={contextValue}>{children}</ApiContext.Provider>
  );
};
