// src/hooks/use-user-query-search-api.tsx
import { useQuery } from '@tanstack/react-query';
import ApiClient from '../config/api-client';

const fetchUserQuery = async (query: string): Promise<string> => {
  const response = await ApiClient.get<{ result: string }>('/search', {
    params: { q: query },
  });

  return response.data.result;
};

export const useUserQuerySearchApi = (query: string) => {
  return useQuery({
    queryKey: ['userQuery', query],
    queryFn: () => fetchUserQuery(query),
    enabled: !!query, // Only fetch if query is non-empty
    staleTime: 1000 * 60,
  });
};
