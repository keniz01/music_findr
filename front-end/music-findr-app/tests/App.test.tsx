import { render, screen } from '@testing-library/react';
import { describe, it, expect, beforeEach } from 'vitest';
import { type RenderResult } from '@testing-library/react';
import App from '../src/App';

describe('App', () => {
  let renderResult: RenderResult;

  beforeEach(() => {
    renderResult = render(<App />);
  });

  it('renders initial content', () => {
    const heading = screen.getByText('Music Findr');
    expect(heading).toBeInTheDocument();
    expect(heading).toBeVisible();
  });
});
