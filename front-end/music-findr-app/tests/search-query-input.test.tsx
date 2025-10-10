import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import React from "react";
import { InputRef } from "antd";
import SearchQueryInput from "../src/components/search/search-query-input";

describe("SearchQueryInput", () => {
  it("renders correctly with default props", () => {
    render(<SearchQueryInput onSearch={() => {}} />);

    const input = screen.getByPlaceholderText("Search...");
    expect(input).toBeInTheDocument();
  });

  it("calls onChange when input value changes", () => {
    const handleChange = vi.fn();
    render(
      <SearchQueryInput value="" onChange={handleChange} onSearch={() => {}} />,
    );

    const input = screen.getByPlaceholderText("Search...") as HTMLInputElement;

    fireEvent.change(input, { target: { value: "test" } });
    expect(handleChange).toHaveBeenCalledTimes(1);
  });

  it("calls onSearch when search icon/button is clicked", () => {
    const handleSearch = vi.fn();
    render(<SearchQueryInput onSearch={handleSearch} />);

    const button = screen.getByRole("button"); // This finds the search icon button
    fireEvent.click(button);
    expect(handleSearch).toHaveBeenCalledTimes(1);
  });

  it("supports ref forwarding", () => {
    const ref = React.createRef<InputRef>();
    render(<SearchQueryInput ref={ref} onSearch={() => {}} />);

    expect(ref.current).not.toBeNull();
    expect(typeof ref.current!.focus).toBe("function");
  });
});
