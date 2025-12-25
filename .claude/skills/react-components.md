# React Component Developer

Build React components for CCM tools. Use when creating components for the LLM Advisor or future React applications.

## You Are

A React developer at CCM who built the LLM Advisor. You know the exact patterns: functional components, PropTypes, hooks, and Tailwind styling.

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
                  : 'bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700'
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

## File Structure

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
│   └── helpers.js
├── data/
│   └── decisionTree.js
├── App.jsx
└── index.jsx
```

## Hooks Patterns

**useReducer for complex state:**
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
      return {
        ...state,
        currentStep: previousStep,
        history: newHistory,
      };
    case 'SET_ANSWER':
      return {
        ...state,
        answers: { ...state.answers, [action.question]: action.answer },
      };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
}

const [state, dispatch] = React.useReducer(reducer, initialState);
```

**Custom hooks:**
```jsx
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}
```

## PropTypes Reference

```jsx
ComponentName.propTypes = {
  // Primitives
  string: PropTypes.string,
  number: PropTypes.number,
  bool: PropTypes.bool,
  func: PropTypes.func,

  // Required
  required: PropTypes.string.isRequired,

  // Arrays
  arrayOfStrings: PropTypes.arrayOf(PropTypes.string),
  arrayOfObjects: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string,
  })),

  // Objects
  object: PropTypes.shape({
    id: PropTypes.string,
    data: PropTypes.object,
  }),

  // Enums
  status: PropTypes.oneOf(['pending', 'active', 'completed']),

  // Union types
  content: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.element,
  ]),

  // Children
  children: PropTypes.node,
};
```

## Tailwind Patterns

**Responsive:**
```jsx
<div className="p-4 md:p-6 lg:p-8">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

**Dark mode:**
```jsx
<div className="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
```

**Interactive states:**
```jsx
<button className="
  px-4 py-2 rounded-lg
  bg-[#CA3553] text-white
  hover:bg-[#b02e4a]
  active:bg-[#9a2840]
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors
">
```

**Focus states (accessibility):**
```jsx
<input className="
  w-full px-4 py-2 rounded-lg border
  focus:outline-none focus:ring-2 focus:ring-[#CA3553] focus:border-transparent
">
```

## Error Boundary

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 text-center">
          <h2 className="text-xl font-semibold text-red-600 mb-4">
            Something went wrong
          </h2>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
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
// __tests__/Component.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ComponentName from '../ComponentName';

describe('ComponentName', () => {
  it('renders title', () => {
    render(<ComponentName title="Test" items={[]} onSelect={() => {}} />);
    expect(screen.getByText('Test')).toBeInTheDocument();
  });

  it('calls onSelect when item clicked', () => {
    const onSelect = vi.fn();
    const items = [{ id: '1', name: 'Item 1' }];
    render(<ComponentName title="Test" items={items} onSelect={onSelect} />);

    fireEvent.click(screen.getByText('Item 1'));
    expect(onSelect).toHaveBeenCalledWith('1');
  });
});
```

## Component Constraints

- Maximum 300 lines per component
- One component per file
- Default exports only
- Functional components (class only for ErrorBoundary)
- Mobile-first responsive design
- No inline styles (use Tailwind)
