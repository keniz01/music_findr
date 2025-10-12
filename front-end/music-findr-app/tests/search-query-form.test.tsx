import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SearchQueryForm from "../src/components/search/search-query-form";
import { beforeEach, describe, expect, it, Mock, vi } from "vitest";

vi.mock("../src/hooks/use-search-query-api", () => ({
  useSearchQueryApi: vi.fn()
}));
import { useSearchQueryApi } from "../src/hooks/use-search-query-api";
const mockedUseSearchQueryApi = useSearchQueryApi as unknown as Mock;

vi.mock("@ant-design/icons", async (importOriginal) => {
  const actual: object = await importOriginal();
  return {
    ...actual,
    CloseOutlined: () => <span>CloseIcon</span>
  };
});

describe("SearchQueryForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders initial form state (no interaction)", () => {
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: false,
      error: null,
      refetch: vi.fn()
    });
    render(<SearchQueryForm />);
    // The input and search button should be there
    expect(screen.getByPlaceholderText("Find music ...")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /search/i })).toBeInTheDocument();
    expect(screen.queryByText(/CloseIcon/i)).not.toBeInTheDocument();
  });

  it("does not trigger refetch when submitting blank or whitespace input", async () => {
    const refetch = vi.fn();
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: false,
      error: null,
      refetch
    });
    render(<SearchQueryForm />);

    const input = screen.getByPlaceholderText("Find music ...");
    const button = screen.getByRole("button", { name: /search/i });

    fireEvent.change(input, { target: { value: "   " } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(refetch).not.toHaveBeenCalled();
    });
  });

  it("triggers refetch when submitting a valid query", async () => {
    const refetch = vi.fn();
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: false,
      error: null,
      refetch
    });
    render(<SearchQueryForm />);

    const input = screen.getByPlaceholderText("Find music ...");
    const button = screen.getByRole("button", { name: /search/i });

    fireEvent.change(input, { target: { value: "hello world" } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(refetch).toHaveBeenCalledTimes(1);
    });
  });

  it("displays loading state when isLoading is true", async () => {
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: true,
      isError: false,
      error: null,
      refetch: vi.fn()
    });
    render(<SearchQueryForm />);

    expect(
      await screen.queryByTestId("search-query-results")
    ).toBeInTheDocument();
  });

  it("displays error when isError is true", async () => {
    const err = new Error("Something went wrong");
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: true,
      error: err,
      refetch: vi.fn()
    });
    render(<SearchQueryForm />);

    // We expect SearchError to show an error message
    // Adjust according to your SearchError implementation
    expect(await screen.findByText(/Search Error/i)).toBeInTheDocument();
    expect(
      await screen.findByText(/Something went wrong/i)
    ).toBeInTheDocument();
  });

  it("shows returned data in chat history after successful fetch", async () => {
    const refetch = vi.fn();
    // First call: no data
    // Then after query set, data arrives
    mockedUseSearchQueryApi.mockReturnValue({
      data: "Mocked result data",
      isLoading: false,
      isError: false,
      error: null,
      refetch
    });

    render(<SearchQueryForm />);

    const input = screen.getByPlaceholderText("Find music ...");
    const button = screen.getByRole("button", { name: /search/i });

    fireEvent.change(input, { target: { value: "test query" } });
    fireEvent.click(button);

    // Wait for chat history to contain the response
    await waitFor(() => {
      // More robust: search for an element whose textContent includes the response
      const found = screen.getAllByText((content, element) => {
        return element?.textContent?.includes("Mocked result data");
      });
      expect(found.length).toBeGreaterThan(0);
    });
  });

  it("clears the input and resets searchQuery when onClear is called", async () => {
    const refetch = vi.fn();
    mockedUseSearchQueryApi.mockReturnValue({
      data: null,
      isLoading: false,
      isError: false,
      error: null,
      refetch
    });

    render(<SearchQueryForm />);

    const input = screen.getByPlaceholderText("Find music ...");

    // Type into the input
    fireEvent.change(input, { target: { value: "some text" } });
    expect((input as HTMLInputElement).value).toBe("some text");

    // Click the clear button
    const clearButton = screen.getByTestId("clear-button");
    fireEvent.click(clearButton);

    // Input should be cleared
    expect((input as HTMLInputElement).value).toBe("");

    // Optionally verify that refetch is not called
    expect(refetch).not.toHaveBeenCalled();
  });
});
