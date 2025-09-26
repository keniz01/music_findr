import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import QuerySearchForm from "./components/search-query-form";
import { ApiProvider } from "./config/api-provider";

const queryClient = new QueryClient();

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <ApiProvider>
      <QuerySearchForm />
    </ApiProvider>
  </QueryClientProvider>
);

export default App;
