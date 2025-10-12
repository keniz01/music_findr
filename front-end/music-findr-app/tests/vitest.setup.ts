import "@testing-library/jest-dom";
import { afterEach, beforeAll } from "vitest";
import { cleanup } from "@testing-library/react";
import React from "react";

// -----------------------------
// ✅ GLOBAL MOCKS & POLYFILLS
// -----------------------------

// Mock `window.matchMedia` for libraries like Ant Design
if (!window.matchMedia) {
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: (query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(), // deprecated
      removeListener: vi.fn(), // deprecated
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn()
    })
  });
}

// Stub heavy icon components, keep accessible name for search button
vi.mock("@ant-design/icons", () => ({
  SearchOutlined: () =>
    React.createElement("span", { role: "img", "aria-label": "search" }),
  CloseCircleFilled: () =>
    React.createElement("span", { role: "img", "aria-label": "close-circle" })
}));

// Optionally stub heavy antd components not directly under test
// This keeps render lightweight while preserving behavior we rely on
vi.mock("antd", async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    // keep Input.Search behavior but avoid heavy internals
    Input: {
      ...actual.Input
    },
    // render minimal alert content so tests can assert text
    Alert: ({
      message,
      description
    }: {
      message?: string;
      description?: string;
    }) =>
      React.createElement(
        "div",
        { role: "alert" },
        React.createElement("div", null, message),
        React.createElement("div", null, description)
      )
  };
});

// -----------------------------
// ✅ GLOBAL LIFECYCLE HOOKS
// -----------------------------

beforeAll(() => {
  // Optional: global setup before all tests
  // e.g., setting up global config, spies, etc.
});

afterEach(() => {
  // Clean up the DOM after each test
  cleanup();
});
