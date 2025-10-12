import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import QuerySearchForm from "./components/search/search-query-form";
import { ApiProvider } from "./config/api-provider";
import Layout from "./components/layout";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const queryClient = new QueryClient();

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <ReactQueryDevtools initialIsOpen={false} />
    <ApiProvider>
      <div className="relative">
        <Layout title="Music Findr">
          <QuerySearchForm />
        </Layout>
      </div>
    </ApiProvider>
  </QueryClientProvider>
);

export default App;
