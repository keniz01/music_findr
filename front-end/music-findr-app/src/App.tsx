import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import UserQuerySearcher from './components/user-query-searcher';

const queryClient = new QueryClient();

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <UserQuerySearcher />
  </QueryClientProvider>
);

export default App;
