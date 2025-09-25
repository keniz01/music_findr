import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import QuerySearchForm from "./components/query-search-form";

const queryClient = new QueryClient();

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <QuerySearchForm />
  </QueryClientProvider>
);

export default App;
