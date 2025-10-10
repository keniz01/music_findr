import { useQuery } from "@tanstack/react-query";
import type { ApiResponse } from "../models/api-response";
import { useApi } from "../config/api-context";
import type { AxiosError } from "axios";

export const useSearchQueryApi = (searchQuery: string) => {
  const { apiClient } = useApi();

  const fetchSearchQueryResult = async (): Promise<string | undefined> => {
    try {
      const { data } = await apiClient.post<ApiResponse<string>>("/api/search", {
        query: searchQuery.trim(),
      });

      if (data?.error) {
        throw new Error(data.error);
      }

      return data?.result;
    } catch (err: unknown) {
      const axiosError = err as AxiosError<{ error: string }>;
      const message =
        axiosError?.response?.data?.error ||
        axiosError?.message ||
        "An unexpected error occurred";

      throw new Error(message);
    }
  };

  return useQuery({
    queryKey: ["fetchSearchQueryResult", searchQuery],
    queryFn: fetchSearchQueryResult,
    enabled: false,
    staleTime: 1000 * 60,
  });
};
