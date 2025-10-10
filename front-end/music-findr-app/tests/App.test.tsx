import { render, screen } from "@testing-library/react";
import { describe, it, expect, beforeEach } from "vitest";
import App from "../src/app";

describe("App", () => {
  beforeEach(() => {
    render(<App />);
  });

  it("renders initial content", () => {
    const heading = screen.getByText("Music Findr");
    expect(heading).toBeInTheDocument();
    expect(heading).toBeVisible();
  });
});
