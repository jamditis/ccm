# React Component Developer

---
description: Build React components for the LLM Advisor and future React applications
activation_triggers:
  - "create React component"
  - "build component"
  - "React pattern"
  - "LLM Advisor component"
related_skills:
  - journalism-tool-builder
---

## When to Use

- Creating components for `/tools/llm-advisor/`
- Building new React applications with build steps (Vite)
- Need PropTypes, hooks, and proper component architecture

## When NOT to Use

- Building browser-based tools without build step (use journalism-tool-builder)
- Creating reports or dashboards (use report-generator)
- Single-file tools (use journalism-tool-builder)

## You Are

A React developer at CCM who built the LLM Advisor. You know the exact patterns: functional components, PropTypes for validation, hooks for state, and Tailwind for styling. No class components except ErrorBoundary.

## Component Structure

```
/tools/llm-advisor/src/
├── components/
│   ├── Header.jsx
│   ├── QuestionView.jsx
│   ├── RecommendationView.jsx
│   ├── ToolCard.jsx
│   ├── ErrorBoundary.jsx
│   └── index.js
├── utils/
├── data/
├── App.jsx
└── index.jsx
```

## Component Template

```jsx
import React, { useState, useMemo, useCallback } from 'react';
import PropTypes from 'prop-types';

function ComponentName({ title, items, onSelect, className = '' }) {
  const [selectedId, setSelectedId] = useState(null);

  // Memoize expensive computations
  const sortedItems = useMemo(() =>
    [...items].sort((a, b) => a.name.localeCompare(b.name)),
    [items]
  );

  // Memoize callbacks passed to children
  const handleSelect = useCallback((id) => {
    setSelectedId(id);
    onSelect(id);
  }, [onSelect]);

  return (
    <div className={`p-4 ${className}`}>
      <h2 className="text-xl font-semibold mb-4">{title}</h2>
      <ul className="space-y-2">
        {sortedItems.map(item => (
          <li key={item.id}>
            <button
              onClick={() => handleSelect(item.id)}
              className={`w-full p-3 rounded-lg text-left transition-colors
                ${selectedId === item.id
                  ? 'bg-[#CA3553] text-white'
                  : 'bg-gray-100 hover:bg-gray-200 dark:bg-gray-800'
                }`}
            >
              {item.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

ComponentName.propTypes = {
  title: PropTypes.string.isRequired,
  items: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
  })).isRequired,
  onSelect: PropTypes.func.isRequired,
  className: PropTypes.string,
};

export default ComponentName;
```

## State with useReducer

For complex state (navigation, multi-step forms):

```jsx
const initialState = {
  currentStep: 'start',
  history: [],
  answers: {},
};

function reducer(state, action) {
  switch (action.type) {
    case 'NAVIGATE':
      return {
        ...state,
        currentStep: action.step,
        history: [...state.history, state.currentStep],
      };
    case 'GO_BACK':
      const newHistory = [...state.history];
      const previousStep = newHistory.pop();
      return { ...state, currentStep: previousStep, history: newHistory };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
}

const [state, dispatch] = React.useReducer(reducer, initialState);
```

## PropTypes Reference

```jsx
ComponentName.propTypes = {
  // Required
  title: PropTypes.string.isRequired,

  // Arrays
  items: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string,
  })),

  // Enums
  status: PropTypes.oneOf(['pending', 'active', 'completed']),

  // Functions
  onSelect: PropTypes.func.isRequired,

  // Children
  children: PropTypes.node,
};
```

## Tailwind Patterns

```jsx
// Responsive
<div className="p-4 md:p-6 lg:p-8">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

// Dark mode
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">

// Interactive
<button className="
  px-4 py-2 rounded-lg bg-[#CA3553] text-white
  hover:bg-[#b02e4a] active:bg-[#9a2840]
  disabled:opacity-50 transition-colors
">

// Focus (accessibility)
<input className="
  focus:outline-none focus:ring-2 focus:ring-[#CA3553]
">
```

## Error Boundary

The only class component allowed:

```jsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 text-center">
          <h2 className="text-xl text-red-600 mb-4">Something went wrong</h2>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-gray-200 rounded-lg"
          >
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

## Testing

```jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ComponentName from '../ComponentName';

describe('ComponentName', () => {
  it('renders title', () => {
    render(<ComponentName title="Test" items={[]} onSelect={() => {}} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', () => {
    const onSelect = vi.fn();
    const items = [{ id: '1', name: 'Item 1' }];
    render(<ComponentName title="Test" items={items} onSelect={onSelect} />);
    fireEvent.click(screen.getByText('Item 1'));
    expect(onSelect).toHaveBeenCalledWith('1');
  });
});
```

## Anti-Patterns

| Don't | Why | Do Instead |
|-------|-----|------------|
| Use class components | Outdated pattern | Functional + hooks |
| Skip PropTypes | No validation | Always define PropTypes |
| Inline styles | Hard to maintain | Tailwind classes |
| Skip memoization | Performance issues | useMemo/useCallback for expensive ops |
| Components > 300 lines | Hard to maintain | Split into smaller components |
| Forget key prop in lists | React warnings | Always use unique key |

## Output

Create at: `/tools/llm-advisor/src/components/[ComponentName].jsx`
