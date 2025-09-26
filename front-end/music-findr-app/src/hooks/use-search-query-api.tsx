import { useQuery } from "@tanstack/react-query";
import { useApi } from "../config/api-provider";
import type { ApiResponse } from "../models/api-response";

export const useSearchQueryApi = (searchQuery: string) => {
  const { apiClient } = useApi();

  const fetchSearchQueryResult = async (): Promise<string | undefined> => {
    const { data } = await apiClient.post<ApiResponse<string>>("/api/search", {
      query: searchQuery.trim()
    });

    if (data?.error) {
      throw new Error("Error fetching search results");
    }

    return data?.result;
  };

  return useQuery({
    queryKey: ["fetchSearchQueryResult", searchQuery],
    queryFn: fetchSearchQueryResult,
    enabled: false,
    staleTime: 1000 * 60,
  });
};
