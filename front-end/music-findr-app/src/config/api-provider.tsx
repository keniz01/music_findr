import { useMemo, type ReactNode } from "react";
import ApiClient from "./api-client";
import { ApiContext } from "./api-context";

interface ApiProviderProps {
  children: ReactNode;
}

export const ApiProvider: React.FC<ApiProviderProps> = ({ children }) => {
  const contextValue = useMemo(() => ({ apiClient: ApiClient }), []);

  return (
    <ApiContext.Provider value={contextValue}>{children}</ApiContext.Provider>
  );
};
