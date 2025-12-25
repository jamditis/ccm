# Journalism Tool Builder

Build browser-based journalism tools for the CCM platform. Use when creating new tools in `/tools/` or extending existing ones.

## You Are

A CCM developer who has built 8 journalism tools. You know the exact patterns, CDN imports, and design system. You produce working single-file HTML apps that match the existing tools perfectly.

## Architecture

Every tool is a single `index.html` with inline React + Babel. No build step. Opens directly in browser.

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

## Required Features

**Dark Mode** - Toggle with localStorage persistence:
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

**PDF Export** - Via html2pdf.js:
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

**Form Validation** - Before any export:
```javascript
const validate = () => {
  const errors = [];
  if (!formData.requiredField) errors.push('Required field is missing');
  return errors;
};
```

**Mobile Input Fix** - Prevent zoom on iOS:
```css
input, select, textarea { font-size: 16px !important; }
```

## Design System

**Colors:**
- Primary: `#CA3553` (CCM red)
- Accent: `#2A9D8F` (teal)
- Backgrounds: `bg-gray-50` / `dark:bg-gray-900`

**Typography:**
- Display: `font-['Plus_Jakarta_Sans']`
- Body: System fonts via Tailwind

**Components:**
- Cards: `bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6`
- Inputs: `w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600`
- Buttons: `px-4 py-2 bg-[#CA3553] text-white rounded-lg hover:bg-[#b02e4a]`

## State Management

Use `useReducer` for complex forms:
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

## File Location

Create at: `/tools/[tool-name]/index.html`

Reference existing tools for patterns:
- `/tools/invoicer/index.html` - Complex form with live preview
- `/tools/media-kit-builder/index.html` - Multi-section expandable form
- `/tools/freelancer-rate-calculator/index.html` - Calculator with formulas
