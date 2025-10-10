import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SearchQueryForm from "../src/components/search/search-query-form";
import { beforeEach, describe, expect, it, vi } from "vitest";
import React from "react";

// 🟢 Correctly mock the hook
vi.mock("../src/hooks/use-search-query-api", () => ({
  useSearchQueryApi: vi.fn(),
}));

// 🔄 Re-import after mocking
import { useSearchQueryApi } from "../src/hooks/use-search-query-api";
const mockedUseSearchQueryApi = useSearchQueryApi as unknown as jest.Mock; // 👈 OR vi.Mock

describe("QuerySearchForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the form correctly", () => {
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: false,
      error: null,
      refetch: vi.fn(),
    });

    render(<SearchQueryForm />);
    expect(screen.getByPlaceholderText("Search...")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /search/i })).toBeInTheDocument();
  });

  // it("displays loading spinner when loading", () => {
  //   mockedUseSearchQueryApi.mockReturnValue({
  //     data: null,
  //     isLoading: true,
  //     isError: false,
  //     error: null,
  //     refetch: vi.fn()
  //   });

  //   render(<SearchQueryForm />);
  //   expect(screen.getByRole("spin")).toBeInTheDocument();
  // });

  it("displays results when data is returned", async () => {
    mockedUseSearchQueryApi.mockReturnValue({
      data: "Mocked result data",
      isLoading: false,
      isError: false,
      error: null,
      refetch: vi.fn(),
    });

    render(<SearchQueryForm />);
    expect(await screen.findByText(/Mocked result data/i)).toBeInTheDocument();
  });

  it("displays error when error occurs", async () => {
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: true,
      error: new Error("API Error"),
      refetch: vi.fn(),
    });

    render(<SearchQueryForm />);
    expect(await screen.findByText(/Oops! Something went wrong/i)).toBeInTheDocument();
    expect(await screen.findByText(/Something went wrong\. Please try again\./i)).toBeInTheDocument();
  });

  it("triggers refetch on form submission with valid input", async () => {
    const refetch = vi.fn();

    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: false,
      error: null,
      refetch,
    });

    render(<SearchQueryForm />);
    const input = screen.getByPlaceholderText("Search...");
    const button = screen.getByRole("button", { name: /search/i });

    fireEvent.change(input, { target: { value: "example query" } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(refetch).toHaveBeenCalled();
    });
  });

  it("does not call refetch on empty or whitespace input", async () => {
    const refetch = vi.fn();

    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: false,
      error: null,
      refetch,
    });

    render(<SearchQueryForm />);
    const input = screen.getByPlaceholderText("Search...");
    const button = screen.getByRole("button");

    fireEvent.change(input, { target: { value: "   " } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(refetch).not.toHaveBeenCalled();
    });
  });
});
