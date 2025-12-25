# Journalism Tool Builder

---
description: Build browser-based journalism tools for the CCM platform
activation_triggers:
  - "create a new tool"
  - "build a journalism tool"
  - "add a tool to /tools/"
  - "extend the invoicer"
  - "new HTML tool"
related_skills:
  - react-components
  - report-generator
---

## When to Use

- Creating a new standalone tool in `/tools/`
- Extending or modifying existing browser-based tools
- Building calculators, generators, or form-based utilities for journalists
- Need a tool that works offline with no server dependencies

## When NOT to Use

- Building the LLM Advisor (use react-components skill instead—it has a build step)
- Creating Python analysis scripts (use data-scraper or content-analyzer)
- Building interactive reports (use report-generator skill)
- Need real-time data or API integrations (tools are static/offline)

## You Are

A CCM developer who has built 8 journalism tools. You produce working single-file HTML apps that match existing patterns exactly. No guessing—you know the CDN imports, design tokens, and state patterns.

## Architecture

Single `index.html` with inline React + Babel. No build step. Opens directly in browser.

```html
<!DOCTYPE html>
<html lang="en" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Tool Name] - CCM Journalism Tools</title>
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-gray-50 dark:bg-gray-900 min-h-full">
  <div id="root"></div>
  <script type="text/babel">
    // React app here
  </script>
</body>
</html>
```

## Required Patterns

**Dark Mode** (every tool has this):
```javascript
const [darkMode, setDarkMode] = React.useState(() => {
  return localStorage.getItem('darkMode') === 'true' ||
    window.matchMedia('(prefers-color-scheme: dark)').matches;
});
React.useEffect(() => {
  document.documentElement.classList.toggle('dark', darkMode);
  localStorage.setItem('darkMode', darkMode);
}, [darkMode]);
```

**PDF Export** (most tools have this):
```javascript
const exportPDF = () => {
  const element = document.getElementById('export-content');
  html2pdf().set({
    margin: 0.5,
    filename: 'document.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
  }).from(element).save();
};
```

**Form Validation** (before export):
```javascript
const validate = () => {
  const errors = [];
  if (!formData.requiredField) errors.push('Required field is missing');
  return errors;
};
```

## Design Tokens

| Element | Value |
|---------|-------|
| Primary | `#CA3553` (CCM red) |
| Accent | `#2A9D8F` (teal) |
| Cards | `bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6` |
| Inputs | `w-full px-4 py-2 border rounded-lg dark:bg-gray-700` |
| Buttons | `px-4 py-2 bg-[#CA3553] text-white rounded-lg hover:bg-[#b02e4a]` |

**Critical**: Input font-size must be 16px+ to prevent iOS zoom:
```css
input, select, textarea { font-size: 16px !important; }
```

## State Management

Use `useReducer` for forms with multiple fields or dynamic items:
```javascript
const initialState = { field1: '', field2: '', items: [] };
function reducer(state, action) {
  switch (action.type) {
    case 'SET_FIELD': return { ...state, [action.field]: action.value };
    case 'ADD_ITEM': return { ...state, items: [...state.items, action.item] };
    default: return state;
  }
}
const [state, dispatch] = React.useReducer(reducer, initialState);
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Create separate CSS file | Inline Tailwind classes |
| Use npm packages | Use CDN imports |
| Build React with JSX compiler | Use Babel standalone in-browser |
| Skip dark mode | Every tool supports dark mode |
| Use font-size < 16px on inputs | Always 16px minimum |
| Forget validation before PDF export | Validate, show errors, then export |

## Reference Implementations

| Tool | Pattern | Location |
|------|---------|----------|
| Invoicer | Complex form + live preview | `/tools/invoicer/index.html` |
| Media Kit Builder | Multi-section expandable | `/tools/media-kit-builder/index.html` |
| Rate Calculator | Formulas + calculations | `/tools/freelancer-rate-calculator/index.html` |

## Output

Create at: `/tools/[tool-name]/index.html`
