# Tool Generator

---
description: Generate new journalism browser tools for the CCM platform with full integration
activation_triggers:
  - "generate a new tool"
  - "create tool generator"
  - "scaffold a journalism tool"
  - "new browser tool with tests"
  - "tool with shared utilities"
related_skills:
  - journalism-tool-builder
  - react-components
---

## When to Use This Skill

Use this skill when you need to:
- Generate a complete new journalism tool from scratch
- Scaffold a tool with all integrations (shared utilities, manifest, README, tests)
- Create either HTML-based (single-file) or React-based (with build) tools
- Ensure consistency with existing CCM tool patterns

This skill provides a **step-by-step generator** that templates from existing tools and integrates all necessary components.

## When NOT to Use This Skill

- Modifying existing tools (use journalism-tool-builder instead)
- Creating Python scripts or backend services
- Building the LLM Advisor specifically (it has unique architecture)
- Quick prototypes without full integration needs

## Tool Type Decision Matrix

| Question | HTML-Based | React-Based |
|----------|------------|-------------|
| Needs build process? | No | Yes |
| Complex state management? | Simple (useState) | Complex (useReducer/context) |
| Multiple components? | Few (<5) | Many (5+) |
| Testing required? | Manual | Unit + Integration |
| Bundle size concern? | No (CDN) | Yes (optimized) |
| Examples | Invoicer, Budget Calculator | LLM Advisor |

**Default choice**: Start with HTML-based unless requirements clearly indicate React-based.

## Step-by-Step Tool Generation Process

### Phase 1: Planning & Setup

#### 1.1 Define Tool Specifications

Ask the user to confirm:
- **Tool name** (kebab-case, e.g., "grant-proposal-generator")
- **Tool purpose** (1-2 sentence description)
- **Primary features** (list 3-5 key features)
- **Tool type** (HTML-based or React-based)
- **Export format** (PDF, CSV, JSON, etc.)
- **Data persistence** (localStorage profiles/settings)

#### 1.2 Create Directory Structure

**For HTML-based tools:**
```bash
mkdir -p /home/user/ccm/tools/[tool-name]
```

**For React-based tools:**
```bash
mkdir -p /home/user/ccm/tools/[tool-name]/{src,components,utils,data}
```

### Phase 2: Template Generation

#### 2.1 HTML-Based Tool Template

Generate `/tools/[tool-name]/index.html` using this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Tool Display Name] | Center for Cooperative Media</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- React & DOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- PDF Export (if needed) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

    <!-- Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        'body': ['"Plus Jakarta Sans"', 'sans-serif'],
                    },
                    colors: {
                        ccm: {
                            red: '#CA3553',
                            teal: '#2A9D8F',
                        }
                    }
                }
            }
        }
    </script>

    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Mobile Input Fix - Prevent iOS Zoom */
        @media screen and (max-width: 768px) {
            input, select, textarea { font-size: 16px !important; }
        }

        /* Print Styles */
        @media print {
            @page { margin: 0; size: auto; }
            .no-print { display: none !important; }
        }
    </style>
</head>
<body class="min-h-screen bg-gray-50 dark:bg-gray-900">

    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useReducer } = React;

        // ===== SHARED UTILITIES INTEGRATION =====

        // Storage Handler (from /tools/shared/utils/storage.js)
        const createStorageHandler = (prefix) => ({
            save(key, data) {
                try {
                    localStorage.setItem(`${prefix}_${key}`, JSON.stringify(data));
                    return true;
                } catch (error) {
                    console.error('Storage save failed:', error);
                    return false;
                }
            },
            load(key, defaultValue = null) {
                try {
                    const data = localStorage.getItem(`${prefix}_${key}`);
                    return data ? JSON.parse(data) : defaultValue;
                } catch (error) {
                    console.error('Storage load failed:', error);
                    return defaultValue;
                }
            },
            remove(key) {
                try {
                    localStorage.removeItem(`${prefix}_${key}`);
                    return true;
                } catch (error) {
                    return false;
                }
            }
        });

        // Error Handler (from /tools/shared/utils/errorHandling.js)
        const createErrorHandler = (showToast) => ({
            async wrapAsync(operation, options = {}) {
                const { errorMessage = 'An error occurred', successMessage = null } = options;
                try {
                    const result = await operation();
                    if (successMessage) showToast(successMessage, 'success');
                    return result;
                } catch (error) {
                    console.error('Operation failed:', error);
                    showToast(errorMessage, 'error');
                    return null;
                }
            },
            async exportPDF(element, options = {}) {
                const { filename = 'export.pdf', onStart = null, onComplete = null } = options;
                if (!element) {
                    showToast('Export element not found', 'error');
                    return false;
                }
                if (onStart) onStart();
                try {
                    await window.html2pdf().set({
                        margin: 0.5,
                        filename,
                        image: { type: 'jpeg', quality: 0.98 },
                        html2canvas: { scale: 2, useCORS: true, logging: false },
                        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
                    }).from(element).save();
                    showToast('PDF exported successfully', 'success');
                    if (onComplete) onComplete();
                    return true;
                } catch (error) {
                    console.error('PDF export failed:', error);
                    showToast('PDF export failed', 'error');
                    if (onComplete) onComplete();
                    return false;
                }
            }
        });

        // Validator (from /tools/shared/utils/validation.js)
        const createValidator = () => ({
            required(value, fieldName) {
                const isValid = value !== null && value !== undefined && value !== '';
                return { isValid, error: isValid ? null : `${fieldName} is required` };
            },
            positiveNumber(value, fieldName) {
                const num = parseFloat(value);
                const isValid = !isNaN(num) && num >= 0;
                return { isValid, error: isValid ? null : `${fieldName} must be a positive number` };
            },
            combine(validations) {
                const errors = validations.filter(v => !v.isValid).map(v => v.error);
                return { isValid: errors.length === 0, errors };
            }
        });

        // ===== MAIN APPLICATION =====

        const [ToolName]App = () => {
            // Dark Mode
            const [darkMode, setDarkMode] = useState(() => {
                return localStorage.getItem('darkMode') === 'true' ||
                    window.matchMedia('(prefers-color-scheme: dark)').matches;
            });

            useEffect(() => {
                document.documentElement.classList.toggle('dark', darkMode);
                localStorage.setItem('darkMode', darkMode);
            }, [darkMode]);

            // Toast notifications
            const [toasts, setToasts] = useState([]);
            const showToast = (message, type = 'info') => {
                const id = Date.now();
                setToasts(prev => [...prev, { id, message, type }]);
                setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4000);
            };

            // Initialize utilities
            const storage = createStorageHandler('[tool-name]');
            const errorHandler = createErrorHandler(showToast);
            const validator = createValidator();

            // State
            const [formData, setFormData] = useState(() =>
                storage.load('formData', {
                    // Define your form fields here
                })
            );

            // Auto-save
            useEffect(() => {
                const timer = setTimeout(() => storage.save('formData', formData), 1000);
                return () => clearTimeout(timer);
            }, [formData]);

            // Handlers
            const handleExport = () => {
                const validation = validator.combine([
                    // Add your validations here
                ]);

                if (!validation.isValid) {
                    validation.errors.forEach(err => showToast(err, 'error'));
                    return;
                }

                errorHandler.exportPDF(
                    document.getElementById('export-content'),
                    {
                        filename: '[tool-name].pdf',
                        onStart: () => showToast('Generating PDF...', 'info')
                    }
                );
            };

            return (
                <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                    {/* Header */}
                    <header className="bg-white dark:bg-gray-800 shadow-sm no-print">
                        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                            <div className="flex justify-between items-center">
                                <div>
                                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                                        [Tool Display Name]
                                    </h1>
                                    <p className="text-gray-600 dark:text-gray-400 mt-1">
                                        [Tool description]
                                    </p>
                                </div>
                                <button
                                    onClick={() => setDarkMode(!darkMode)}
                                    className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600"
                                >
                                    {darkMode ? '☀️' : '🌙'}
                                </button>
                            </div>
                        </div>
                    </header>

                    {/* Main Content */}
                    <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                            {/* Left: Form */}
                            <div className="space-y-6">
                                <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                                    <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
                                        Input
                                    </h2>
                                    {/* Add your form fields here */}
                                </div>

                                <button
                                    onClick={handleExport}
                                    className="w-full px-6 py-3 bg-[#CA3553] text-white rounded-lg hover:bg-[#b02e4a] font-semibold"
                                >
                                    Export PDF
                                </button>
                            </div>

                            {/* Right: Preview */}
                            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
                                <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white no-print">
                                    Preview
                                </h2>
                                <div id="export-content" className="bg-white p-8">
                                    {/* Add your preview/export content here */}
                                </div>
                            </div>
                        </div>
                    </main>

                    {/* Toast Notifications */}
                    <div className="fixed bottom-4 right-4 space-y-2 z-50 no-print">
                        {toasts.map(toast => (
                            <div
                                key={toast.id}
                                className={`px-4 py-3 rounded-lg shadow-lg text-white ${
                                    toast.type === 'error' ? 'bg-red-500' :
                                    toast.type === 'success' ? 'bg-green-500' :
                                    'bg-blue-500'
                                }`}
                            >
                                {toast.message}
                            </div>
                        ))}
                    </div>

                    {/* Footer */}
                    <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 mt-16 border-t border-gray-200 dark:border-gray-700 no-print">
                        <p className="text-center text-sm text-gray-600 dark:text-gray-400">
                            © 2025 <a href="https://centerforcooperativemedia.org/" target="_blank" rel="noopener noreferrer" className="hover:text-[#CA3553]">Center for Cooperative Media</a>
                        </p>
                    </footer>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<[ToolName]App />);
    </script>
</body>
</html>
```

#### 2.2 React-Based Tool Template

For React-based tools, generate the following files:

**package.json:**
```json
{
  "name": "[tool-name]",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint . --ext js,jsx"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "@vitest/ui": "^1.0.0",
    "autoprefixer": "^10.4.17",
    "eslint": "^8.57.0",
    "eslint-plugin-react": "^7.34.1",
    "eslint-plugin-react-hooks": "^4.6.0",
    "jsdom": "^23.0.0",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "vite": "^5.2.0",
    "vitest": "^1.0.0"
  }
}
```

**vite.config.js:**
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/tools/[tool-name]/'
});
```

**vitest.config.js:**
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/__tests__/setup.js'],
    include: ['src/**/*.{test,spec}.{js,jsx}'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'src/__tests__/']
    }
  }
});
```

**tailwind.config.js:**
```javascript
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        ccm: {
          red: '#CA3553',
          teal: '#2A9D8F'
        }
      }
    }
  },
  plugins: []
};
```

**src/__tests__/setup.js:**
```javascript
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

afterEach(() => {
  cleanup();
});
```

**src/App.test.jsx:**
```javascript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/[Tool Name]/i)).toBeDefined();
  });
});
```

### Phase 3: Shared Utilities Integration

#### 3.1 For HTML-Based Tools

The shared utilities are inlined in the template above. Ensure they include:
- ✅ `createStorageHandler()` - localStorage wrapper
- ✅ `createErrorHandler()` - error handling with toast
- ✅ `createValidator()` - form validation
- ✅ Dark mode toggle
- ✅ Toast notification system

#### 3.2 For React-Based Tools

Import from shared utilities:
```javascript
import { createStorageHandler } from '../shared/utils/storage';
import { createErrorHandler } from '../shared/utils/errorHandling';
import { createValidator } from '../shared/utils/validation';
import { createI18n } from '../shared/utils/i18n';
```

### Phase 4: Manifest Integration

#### 4.1 Update /tools/manifest.json

Read the existing manifest, add the new tool entry, and write it back:

```javascript
// Read existing manifest
const manifestPath = '/home/user/ccm/tools/manifest.json';
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

// Add new tool
manifest.tools = manifest.tools || [];
manifest.tools.push({
  id: "[tool-name]",
  name: "[Tool Display Name]",
  description: "[Tool description]",
  category: "productivity", // or "utilities", "generators", etc.
  path: "/tools/[tool-name]/",
  screenshot: "/screenshots/[tool-name].png",
  tags: ["[tag1]", "[tag2]"]
});

// Write back
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
```

**Categories:**
- `productivity` - Calculators, budgets, rates
- `generators` - Invoices, proposals, media kits
- `utilities` - Charts, validators, converters
- `analysis` - Data processors, decision tools

### Phase 5: Documentation

#### 5.1 Generate README.md

Create `/tools/[tool-name]/README.md`:

```markdown
# [Tool Display Name]

[Brief description of what the tool does and who it's for]

## Features

- **Feature 1**: Description
- **Feature 2**: Description
- **Feature 3**: Description
- **Data Persistence**: Automatically saves your work in browser storage
- **Dark Mode**: Built-in dark mode support
- **Export**: Download as PDF

## Quick Start

1. Open `index.html` in any modern web browser
2. [Step-by-step usage instructions]
3. Click "Export PDF" to download

## Usage Guide

### [Section 1]

[Detailed instructions for using this section]

### [Section 2]

[Detailed instructions for using this section]

## Technical Details

### Dependencies (CDN-loaded)
- React 18
- ReactDOM 18
- Babel (for JSX transformation)
- Tailwind CSS
- html2pdf.js (PDF generation)
- Google Fonts (Plus Jakarta Sans)

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript enabled

### Local Storage
The application uses browser localStorage to persist:
- Form data (auto-saved every second)
- Dark mode preference
- User profiles (if applicable)

## File Structure

```
[tool-name]/
├── index.html    # Complete single-file application
└── README.md     # This documentation
```

## Customization

### Modifying Default Values

Edit the initial state in the main component:

```javascript
const [formData, setFormData] = useState({
    field1: 'default value',
    field2: 0
});
```

### Styling

The tool uses Tailwind CSS. Modify the `tailwind.config` section in the HTML:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                // Add custom colors
            }
        }
    }
}
```

## Troubleshooting

### PDF Not Generating
- Ensure JavaScript is enabled
- Check browser console for errors
- Try a different browser (Chrome recommended)

### Data Not Saving
- Check if localStorage is enabled
- Ensure browser isn't in private/incognito mode
- Check available storage quota

### Styling Issues
- Clear browser cache
- Check internet connection (CDN dependencies)
- Disable browser extensions that might interfere

## Credits

- **Created by**: [Center for Cooperative Media](https://centerforcooperativemedia.org/)
- **Organization**: Montclair State University
- **Year**: 2025

## License

This tool is provided by the Center for Cooperative Media for use in supporting local journalism and media organizations.
```

### Phase 6: Testing Setup

#### 6.1 For HTML-Based Tools

Create a simple test checklist in the README:

```markdown
## Testing Checklist

Manual testing checklist for this tool:

- [ ] Form inputs accept valid data
- [ ] Form validation catches invalid data
- [ ] Dark mode toggle works
- [ ] Data persists in localStorage
- [ ] PDF export generates correctly
- [ ] Mobile responsive (test on phone)
- [ ] Works in Chrome, Firefox, Safari
- [ ] Print styles work correctly
- [ ] No console errors
- [ ] Accessibility (keyboard navigation)
```

#### 6.2 For React-Based Tools

Generate test files:

**src/App.test.jsx:**
```javascript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  it('renders the main heading', () => {
    render(<App />);
    expect(screen.getByText(/[Tool Name]/i)).toBeDefined();
  });

  it('toggles dark mode', () => {
    render(<App />);
    const darkModeButton = screen.getByRole('button', { name: /dark mode/i });
    fireEvent.click(darkModeButton);
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('shows validation errors for invalid input', () => {
    render(<App />);
    // Add specific validation tests
  });

  it('exports PDF successfully', async () => {
    render(<App />);
    // Mock html2pdf and test export
  });
});
```

**src/utils/[utility].test.js:**
```javascript
import { describe, it, expect } from 'vitest';
import { createValidator } from '../../../shared/utils/validation';

describe('Validation Utilities', () => {
  const validator = createValidator();

  it('validates required fields', () => {
    const result = validator.required('', 'Test Field');
    expect(result.isValid).toBe(false);
    expect(result.error).toContain('required');
  });

  it('validates positive numbers', () => {
    const result = validator.positiveNumber(-5, 'Amount');
    expect(result.isValid).toBe(false);
  });
});
```

### Phase 7: Final Checks & Launch

#### 7.1 Pre-launch Checklist

Before considering the tool complete:

- [ ] All files generated in correct locations
- [ ] README.md is complete and accurate
- [ ] manifest.json updated with new tool entry
- [ ] Shared utilities properly integrated
- [ ] Dark mode working
- [ ] localStorage persistence working
- [ ] PDF export functioning (if applicable)
- [ ] Mobile responsive (16px+ inputs)
- [ ] No console errors
- [ ] Browser compatibility tested
- [ ] Tests passing (for React-based tools)

#### 7.2 Announce Completion

Provide the user with:
1. **Tool location**: `/home/user/ccm/tools/[tool-name]/`
2. **How to test**: `open /home/user/ccm/tools/[tool-name]/index.html`
3. **For React tools**: Instructions to run `npm install && npm run dev`
4. **Next steps**: Suggestions for screenshots, additional features, or deployment

## Design System Reference

### Color Palette

```javascript
colors: {
  ccm: {
    red: '#CA3553',      // Primary brand color
    teal: '#2A9D8F',     // Accent color
  },
  gray: {
    50: '#F9FAFB',       // Light background
    900: '#111827',      // Dark background
    // Standard Tailwind grays
  }
}
```

### Component Patterns

**Card:**
```jsx
<div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6">
  {/* content */}
</div>
```

**Input:**
```jsx
<input
  type="text"
  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-[#CA3553]"
/>
```

**Button (Primary):**
```jsx
<button className="px-6 py-3 bg-[#CA3553] text-white rounded-lg hover:bg-[#b02e4a] font-semibold transition-colors">
  Action
</button>
```

**Button (Secondary):**
```jsx
<button className="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 font-semibold transition-colors">
  Action
</button>
```

### Typography

- **Headings**: Bold, use `font-bold` or `font-semibold`
- **Body**: Regular weight, `text-gray-900 dark:text-white`
- **Secondary text**: `text-gray-600 dark:text-gray-400`
- **Font family**: Plus Jakarta Sans (loaded from Google Fonts)

### Spacing

- **Section gaps**: `space-y-6` or `gap-6`
- **Card padding**: `p-6`
- **Container max-width**: `max-w-7xl`
- **Page padding**: `px-4 sm:px-6 lg:px-8`

## Common Integrations

### i18n (Internationalization)

If tool needs multi-language support:

```javascript
const i18n = createI18n('en'); // or 'es'
const label = i18n.t('common.save'); // "Save"
```

Add translations to `/tools/shared/locales/en.json` and `/tools/shared/locales/es.json`.

### Analytics (Privacy-preserving)

```javascript
import { createAnalytics } from '../shared/utils/analytics';
const analytics = createAnalytics({ enabled: true });
analytics.trackToolUsage('[Tool Name]', 'export');
```

### PWA Support

For offline functionality:

```javascript
import { createPWAHandler } from '../shared/utils/pwa';
const pwa = createPWAHandler({
  onUpdateFound: () => showToast('Update available'),
  onInstallPrompt: (available) => setShowInstall(available)
});
await pwa.register();
```

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do |
|---------|-------|
| Use `<div>` for clickable elements | Use `<button>` for semantic HTML |
| Hardcode colors in JSX | Use Tailwind classes or theme colors |
| Store sensitive data in localStorage | Only store non-sensitive form data |
| Forget mobile styles | Test on mobile, ensure 16px+ inputs |
| Skip error handling | Wrap operations with errorHandler |
| Ignore dark mode | Always implement dark mode toggle |
| Use complex state without reducer | Use useReducer for complex forms |
| Forget validation before export | Validate, show errors, then export |

## Example Workflow

**User request**: "Create a simple expense tracker tool"

**Your response:**

1. **Confirm specs** with user:
   - Tool name: "expense-tracker"
   - Purpose: Track daily expenses by category
   - Features: Add expenses, categorize, view totals, export PDF
   - Type: HTML-based (simple tool)

2. **Create directory**: `/home/user/ccm/tools/expense-tracker/`

3. **Generate files**:
   - `index.html` (from template, customized)
   - `README.md` (comprehensive documentation)

4. **Update manifest**: Add entry to `/tools/manifest.json`

5. **Integrate utilities**:
   - Storage for saving expenses
   - Validator for expense amounts
   - Error handler for PDF export

6. **Test checklist**: Provide manual testing checklist

7. **Announce**: "✅ Expense Tracker created at `/home/user/ccm/tools/expense-tracker/`. Open `index.html` to test!"

## Key Success Criteria

A well-generated tool should:
- ✅ Work immediately when opened (no build errors)
- ✅ Have consistent styling with other CCM tools
- ✅ Include dark mode support
- ✅ Save user data in localStorage
- ✅ Validate inputs before export
- ✅ Be mobile-responsive
- ✅ Have comprehensive README
- ✅ Be listed in manifest.json
- ✅ Follow accessibility best practices
- ✅ Have no console errors

## Reference Tools

Study these for patterns:

| Tool | Location | Learn From |
|------|----------|------------|
| Invoicer | `/tools/invoicer/` | Complex forms, live preview, AI integration |
| Budget Calculator | `/tools/event-budget-calculator/` | Calculations, validation, totals |
| Media Kit Builder | `/tools/media-kit-builder/` | Multi-section forms, expandable sections |
| LLM Advisor | `/tools/llm-advisor/` | React + Vite setup, testing, components |

## Summary

This skill provides a complete, step-by-step process for generating journalism tools that:
1. Follow CCM design patterns
2. Integrate with shared utilities
3. Include proper documentation
4. Update the manifest automatically
5. Have testing configurations
6. Work out of the box

Always prioritize user experience, accessibility, and code quality. Generate tools that journalists can trust and use daily.
