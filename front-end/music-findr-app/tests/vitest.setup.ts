/// <reference types="./types.d.ts" />
import "@testing-library/jest-dom";
import { afterEach, beforeAll } from "vitest";
import { cleanup } from "@testing-library/react";

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
      dispatchEvent: vi.fn(),
    }),
  });
}

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
