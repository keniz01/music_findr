import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useSearchQueryApi } from "../src/hooks/use-search-query-api";
import { ApiContext } from "../src/config/api-context";
import React from "react";
import { AxiosInstance } from "axios";

const postMock = vi.fn();

// Provide ApiContext value for tests
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <ApiContext.Provider value={{ apiClient: { post: postMock } as AxiosInstance }}>
        {children}
      </ApiContext.Provider>
    </QueryClientProvider>
  );
};

describe("useSearchQueryApi", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns result on successful fetch", async () => {
    const mockResult = "Search result";

    postMock.mockResolvedValueOnce({
      data: {
        result: mockResult,
        error: null,
      },
    });

    const { result } = renderHook(() => useSearchQueryApi("test query"), {
      wrapper: createWrapper(),
    });

    const { data, error } = await result.current.refetch();

    expect(postMock).toHaveBeenCalledWith("/api/search", {
      query: "test query",
    });
    expect(data).toBe(mockResult);
    expect(error).toBeNull();
  });

  it("throws error on API error response", async () => {
    postMock.mockResolvedValueOnce({
      data: {
        result: null,
        error: "Something went wrong",
      },
    });

    const { result } = renderHook(() => useSearchQueryApi("bad query"), { wrapper: createWrapper() });

    let refetchResult: Awaited<ReturnType<typeof result.current.refetch>>;

    await waitFor(async () => {
      refetchResult = await result.current.refetch({ throwOnError: false });
      expect(refetchResult.error).toBeDefined();
    });

    expect(refetchResult!.data).toBeUndefined();
    expect(refetchResult!.error).toBeInstanceOf(Error);
    expect(refetchResult!.error?.message).toBe("Something went wrong");
  });
});
