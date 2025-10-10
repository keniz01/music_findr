import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import QuerySearchForm from "./components/search/search-query-form";
import { ApiProvider } from "./config/api-provider";
import Layout from "./components/layout";

const queryClient = new QueryClient();

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <ApiProvider>
      <Layout title="Music Findr">
        <QuerySearchForm />
      </Layout>
    </ApiProvider>
  </QueryClientProvider>
);

export default App;
