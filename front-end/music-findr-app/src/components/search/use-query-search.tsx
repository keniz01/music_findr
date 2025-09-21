// hooks/useUser.ts
import { useQuery } from '@tanstack/react-query';

interface IUserQuery {
  query: string;
}

interface IUserQueryResponse {
}

const fetchUser = async (userQuery: string): Promise<IUserQuery> => {
  const { data } = await ApiClient.get(`/api/users/${userQuery}`);
  return data;
};

export const useQuerySearch = (userQuery: string): Promise<IUserQueryResponse> => {
  return useQuery({
    queryKey: ['userQuery', userQuery],   // 🔑 Unique key for caching
    queryFn: () => fetchUser(id),
    staleTime: 1000 * 60 * 5, // ✅ Data stays fresh for 5 minutes
    cacheTime: 1000 * 60 * 10 // 🕒 Data is cached for 10 minutes
  });
};
