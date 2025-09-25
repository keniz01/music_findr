/// <reference types="./types.d.ts" />
import "@testing-library/jest-dom";

beforeAll(() => {
  // Add any global test setup here
});

afterEach(() => {
  // Clean up after each test
  document.body.innerHTML = "";
});
