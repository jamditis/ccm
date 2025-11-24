import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from '../App';

describe('LLM Advisor App', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText(/LLM Journalism Tool Advisor/i)).toBeInTheDocument();
  });

  it('displays initial question', () => {
    render(<App />);
    expect(screen.getByText(/What would you like to do/i)).toBeInTheDocument();
  });

  it('allows navigation through decision tree', () => {
    render(<App />);

    // Click on first option
    const firstOption = screen.getAllByRole('button')[0];
    fireEvent.click(firstOption);

    // Should show new question or results
    expect(screen.getByRole('main')).toBeInTheDocument();
  });

  it('has a restart button', () => {
    render(<App />);
    const restartButton = screen.getByText(/Start Over/i);
    expect(restartButton).toBeInTheDocument();
  });
});

describe('Decision Tree Navigation', () => {
  it('tracks navigation history', () => {
    render(<App />);

    // Navigate forward
    const options = screen.getAllByRole('button');
    fireEvent.click(options[0]);

    // Check if back button appears
    const backButton = screen.queryByText(/Back/i);
    expect(backButton).toBeInTheDocument();
  });
});
