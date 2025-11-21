# Architecture Documentation

This document provides detailed technical documentation of the LLM Journalism Tool Advisor application architecture.

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Component Architecture](#component-architecture)
- [State Management](#state-management)
- [Data Flow](#data-flow)
- [Decision Tree System](#decision-tree-system)
- [Performance Optimizations](#performance-optimizations)
- [Error Handling](#error-handling)

## Overview

The LLM Journalism Tool Advisor is a single-page React application built with modern best practices. The architecture prioritizes:

- **Modularity**: Components are small, focused, and reusable
- **Maintainability**: Clear separation of concerns
- **Performance**: Optimized rendering with memoization
- **Type Safety**: PropTypes validation throughout
- **User Experience**: Graceful error handling and responsive design

## Technology Stack

### Core

- **React 18.2** - UI library with hooks
- **Vite 5.2** - Build tool and dev server
- **JavaScript (ES6+)** - Programming language

### Styling

- **Tailwind CSS 3.4** - Utility-first CSS framework
- **PostCSS** - CSS processing
- **Custom CSS** - App-specific styles and animations

### Development

- **ESLint** - Code linting
- **PropTypes** - Runtime type checking
- **Browserslist** - Browser compatibility

## Project Structure

```
ccm/
├── components/           # React components
│   ├── ErrorBoundary.jsx
│   ├── Header.jsx
│   ├── QuestionView.jsx
│   ├── RecommendationView.jsx
│   └── ToolCard.jsx
├── data/                # Static data
│   └── decisionTree.js  # Decision tree configuration
├── utils/               # Utility functions
│   ├── colorUtils.js
│   └── decisionReducer.js
├── App.jsx              # Main component
├── App.css              # Global styles
├── index.jsx            # Entry point
├── index.css            # Base styles
├── index.html           # HTML template
└── package.json         # Dependencies
```

## Component Architecture

### Component Hierarchy

```
<ErrorBoundary>          # Error handling wrapper
  <App>                  # Main application logic
    <div.container>
      <div.card>
        <Header           # Navigation and progress
          history={history}
          showRecommendation={showRecommendation}
          onBack={handleBack}
          onRestart={handleRestart}
        />
        {showRecommendation ? (
          <RecommendationView   # Tool recommendations
            selectedTools={selectedTools}
            onRestart={handleRestart}
          >
            <ToolCard />        # Individual tool card
          </RecommendationView>
        ) : (
          <QuestionView         # Question display
            question={currentNode.question}
            options={currentNode.options}
            onOptionSelect={handleOptionSelect}
          />
        )}
      </div.card>
    </div.container>
  </App>
</ErrorBoundary>
```

### Component Responsibilities

#### **ErrorBoundary** (`components/ErrorBoundary.jsx`)
- Class component implementing error boundary pattern
- Catches JavaScript errors anywhere in child component tree
- Displays fallback UI when errors occur
- Provides reset/restart functionality
- Shows error details in development mode

#### **App** (`App.jsx`)
- Main application component
- Manages application state with useReducer
- Implements memoization for performance
- Coordinates between view components
- Applies dynamic color themes based on current step

#### **Header** (`components/Header.jsx`)
- Navigation controls (back/restart buttons)
- Progress bar showing completion percentage
- Breadcrumb trail of user selections
- Responsive layout with mobile considerations

#### **QuestionView** (`components/QuestionView.jsx`)
- Displays current question
- Renders option buttons
- Handles option selection events
- Accessible button implementation

#### **RecommendationView** (`components/RecommendationView.jsx`)
- Displays final tool recommendations
- Maps through selected tools
- Renders ToolCard for each recommendation
- Provides restart functionality

#### **ToolCard** (`components/ToolCard.jsx`)
- Individual tool recommendation display
- Shows tool name, description, and recommended tools
- Displays sample prompts
- Includes usage tips
- Color-coded tool badges

## State Management

### State Structure

```javascript
{
  currentStep: string,        // Current node ID in decision tree
  history: Array<{            // Navigation history
    step: string,
    question: string,
    selection: string,
    tools: Array
  }>,
  selectedTools: Array,       // Accumulated tool recommendations
  showRecommendation: boolean // Whether to show final recommendations
}
```

### Actions

```javascript
{
  type: 'SELECT_OPTION',
  payload: {
    option: Object,
    currentQuestion: string,
    decisionTree: Object
  }
}

{
  type: 'GO_BACK'
}

{
  type: 'RESTART'
}
```

### Reducer Logic (`utils/decisionReducer.js`)

**SELECT_OPTION**:
1. Creates history entry with current state
2. Adds tools from option to selectedTools
3. Updates currentStep to option.next
4. Sets showRecommendation if reaching end

**GO_BACK**:
1. Removes last history entry
2. Returns to previous step
3. Rebuilds selectedTools from remaining history
4. Hides recommendation view

**RESTART**:
1. Resets all state to initial values
2. Returns to start node

## Data Flow

### User Interaction Flow

```
User clicks option
    ↓
handleOptionSelect called
    ↓
dispatch(SELECT_OPTION)
    ↓
Reducer updates state
    ↓
Component re-renders with new state
    ↓
useMemo recalculates affected values
    ↓
UI updates with new question or recommendations
```

### Navigation Flow

```
                    ┌─────────┐
                    │  Start  │
                    └────┬────┘
                         │
                    User selects
                         │
                  ┌──────┴──────┐
                  │             │
              Research      Content
                  │             │
            ┌─────┴─────┐      etc...
            │           │
      Basic Topic  Niche Topic
            │           │
       ┌────┴────┐ ┌────┴────┐
       │         │ │         │
    General   Niche   ...   ...
       │         │
       └────┬────┘
            │
     Recommendation
```

## Decision Tree System

### Node Structure

Each node in the decision tree has:

```javascript
{
  question: string,            // Question to display
  options: Array<{
    text: string,              // Option button text
    next: string,              // Next node ID or "recommendation"
    tools?: Array<{            // Optional tool recommendations
      name: string,            // Tool category name
      description: string,     // What it helps with
      tools: Array<string>,    // Specific tool names
      prompt: string,          // Sample prompt template
      tips?: string            // Usage tips
    }>
  }>
}
```

### Tree Traversal

1. App starts at `"start"` node
2. User selects an option
3. App navigates to `option.next` node
4. If `next === "recommendation"`, show final view
5. Otherwise, repeat from step 2

### Adding Nodes

To extend the decision tree:

1. Add new node to `data/decisionTree.js`
2. Reference new node in existing option's `next` field
3. Include tool recommendations as needed
4. Test navigation path

## Performance Optimizations

### Memoization

**useMemo** - Caches computed values:
- `currentNode` - Prevents repeated tree lookups
- `colorClass` - Caches color calculation
- `mainContent` - Caches view component rendering

**useCallback** - Stabilizes function references:
- `handleOptionSelect` - Prevents QuestionView re-renders
- `handleBack` - Stabilizes Header prop
- `handleRestart` - Stabilizes RecommendationView prop

### Why This Matters

Without memoization:
- Child components re-render unnecessarily
- Functions recreated on every render
- Poor performance with complex UIs

With memoization:
- Child components only re-render when props change
- Functions maintain referential equality
- Smooth user experience

## Error Handling

### Error Boundary Strategy

The ErrorBoundary component catches:
- Component render errors
- Lifecycle method errors
- Constructor errors in child components

### Graceful Degradation

When an error occurs:
1. Error boundary catches it
2. User sees friendly error message
3. Option to restart application
4. Developers see error details (dev mode only)
5. Error logged to console

### Best Practices

- All components validate props with PropTypes
- Error boundary wraps entire app at root level
- Errors don't crash the entire application
- Users can recover without losing work

## Future Considerations

### Potential Enhancements

1. **TypeScript Migration**
   - Replace PropTypes with TypeScript interfaces
   - Compile-time type checking
   - Better IDE support

2. **Testing**
   - Unit tests for reducer logic
   - Component tests with React Testing Library
   - E2E tests with Playwright

3. **State Persistence**
   - Save state to localStorage
   - Allow users to resume sessions
   - Export/import functionality

4. **Analytics**
   - Track popular paths through tree
   - Identify drop-off points
   - A/B test different recommendations

5. **Accessibility**
   - Full keyboard navigation
   - Screen reader optimization
   - WCAG 2.1 AA compliance

---

For questions or clarifications, please open an issue on GitHub.
