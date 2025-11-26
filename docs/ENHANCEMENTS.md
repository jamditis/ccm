# CCM Tools Enhancement Summary

> **What is this document?** This explains the behind-the-scenes improvements we've made to make the tools more reliable, easier to use, and better for everyone. Think of it as a list of "upgrades" to the tools' foundation.

> **Who is this for?** Primarily developers who want to understand the technical infrastructure. Regular users don't need to read this—the improvements are already built into the tools you use!

---

## Overview

We've made improvements in several areas to make the tools:
- **More reliable** — Better handling when things go wrong
- **More accessible** — Works in multiple languages
- **More private** — Analytics that don't track personal information
- **More convenient** — Works offline after first visit

Below are the technical details of each improvement.

## 1. Error Handling Framework

**In plain English:** When something goes wrong (like trying to save a file that's too big), instead of the tool crashing or showing a confusing error, it now shows a helpful message explaining what happened and what to do.

**Location:** `tools/shared/utils/errorHandling.js`

Added comprehensive error handling utilities that can be integrated into all tools:

- **PDF Export Protection** - Try/catch wrappers for html2pdf operations with user-friendly error messages
- **localStorage Safety** - Handles quota exceeded errors, parsing failures, and private mode
- **Async Operation Wrappers** - Consistent error handling pattern for all async operations
- **Error Boundary Component** - React error boundary for graceful failure handling

### Usage
```javascript
const { wrapAsync, exportPDF } = createErrorHandler(showToast);
await exportPDF(element, { filename: 'report.pdf' });
```

---

## 2. Input Validation Framework

**In plain English:** The tools now check your input as you type to catch mistakes early. For example, if you accidentally type letters in a number field, or leave a required field blank, the tool will let you know right away instead of failing later.

**Location:** `tools/shared/utils/validation.js`

Created validation utilities for all form inputs:

- **Required Field Validation**
- **Number Range Validation** - Positive numbers, min/max bounds
- **Currency Validation** - Proper currency amount handling
- **Email/Phone Validation**
- **Budget Balance Validation** - Ensures expenses don't exceed revenue
- **Input Sanitization** - Clean and normalize user input

### Usage
```javascript
const validator = createValidator();
const result = validator.combine([
  validator.required(name, 'Event Name'),
  validator.positiveNumber(amount, 'Amount'),
  validator.budgetBalance(expenses, revenue)
]);
```

---

## 3. Testing Infrastructure

**In plain English:** Before releasing updates, we now have automated checks that verify the tools still work correctly. This is like a quality control checklist that runs automatically every time we make changes.

### LLM Advisor Tests
**Location:** `tools/llm-advisor/src/__tests__/`

- Vitest configuration for React testing
- Component tests for App.jsx
- Decision tree navigation tests
- Test setup with mocks for localStorage and matchMedia

### Social Scraper Tests
**Location:** `social-scraper/tests/`

- pytest configuration
- Config module tests
- Scraper unit tests (TikTok, Instagram, YouTube)
- Integration tests for checkpointing and error recovery

### Run Tests
```bash
# LLM Advisor
cd tools/llm-advisor && npm test

# Social Scraper
cd social-scraper && pytest
```

---

## 4. Internationalization (i18n)

**In plain English:** The tools can now display text in different languages. Currently we support English and Spanish, with the ability to add more languages in the future. The tool can automatically detect your browser's language preference.

> **What does "i18n" mean?** It's developer shorthand for "internationalization" (i + 18 letters + n). It refers to making software work in multiple languages.

**Location:** `tools/shared/locales/` and `tools/shared/utils/i18n.js`

Added multi-language support:

- **English** (`en.json`) - Complete translations
- **Spanish** (`es.json`) - Complete translations
- **Browser Detection** - Auto-detect user's preferred language
- **Template Interpolation** - Support for dynamic values in translations

### Supported Languages
- English (en)
- Spanish (es)

### Usage
```javascript
const i18n = createI18n('en');
const label = i18n.t('budget.totalExpenses'); // "Total Expenses"
```

---

## 5. CI/CD Pipeline

**In plain English:** Every time we update the code, automated systems run tests, check for security issues, and prepare preview versions. This helps us catch problems before they reach users.

> **What is CI/CD?** Continuous Integration / Continuous Deployment. It's an automated process that tests and publishes code changes automatically.

**Location:** `.github/workflows/ci.yml`

Automated testing and deployment pipeline:

- **HTML Linting** - Validate all HTML tools
- **React App Testing** - Build and test LLM Advisor
- **Python Testing** - Run pytest for Social Scraper
- **Security Scanning** - Trivy vulnerability scanner
- **Deploy Previews** - Netlify preview deployments for PRs
- **Code Coverage** - Upload to Codecov

### Triggers
- Push to `main` or `develop`
- Pull requests to `main`

---

## 6. Dark Mode Support

**In plain English:** If your computer or phone is set to "dark mode," the tools can now match that preference. This is easier on your eyes in low-light environments and can save battery on some devices.

**Location:** `tools/shared/utils/darkMode.js`

Complete dark mode implementation:

- **System Preference Detection** - Respects OS dark mode setting
- **User Override** - Manual toggle with localStorage persistence
- **Tailwind Integration** - Uses Tailwind's dark mode classes
- **Smooth Transitions** - Animated theme switching

### Usage
```javascript
const darkMode = createDarkModeHandler();
darkMode.init(); // Call on app load
const isDark = darkMode.toggle(); // Toggle theme
```

---

## 7. PWA Configuration

**In plain English:** After visiting a tool once, it can work even without an internet connection. You can also "install" the tools on your phone or computer like a regular app, with its own icon.

> **What is a PWA?** A Progressive Web App is a website that can work like a native app—with offline support, home screen icons, and fast loading.

**Location:** `tools/manifest.json`, `tools/sw.js`, `tools/shared/utils/pwa.js`

Progressive Web App support for offline use:

- **Web App Manifest** - Install prompts, icons, theme colors
- **Service Worker** - Offline caching, background updates
- **Install Prompt Handling** - Custom install UI
- **Update Notifications** - Notify users of new versions

### Features
- Works offline after first visit
- Installable on desktop and mobile
- Automatic cache updates
- Fast subsequent loads

---

## 8. Privacy-Preserving Analytics

**In plain English:** We track basic usage information (like which tools are popular) to improve the tools, but we do it without tracking you personally. No cookies, no personal data, no selling your information.

**Location:** `tools/shared/utils/analytics.js`

Analytics that respect user privacy:

- **No Cookies** - Uses Plausible Analytics approach
- **No Personal Data** - Only aggregated usage data
- **Tool Usage Tracking** - Which tools are used most
- **Export Tracking** - PDF/PNG export usage
- **Error Tracking** - Identify common issues

### Usage
```javascript
const analytics = createAnalytics({ enabled: true });
analytics.trackToolUsage('Invoicer', 'generate');
analytics.trackExport('Budget Calculator', 'PDF');
```

---

## 9. Shared Component Library

**In plain English:** Instead of reinventing the wheel for each tool, we've created a collection of reusable building blocks. This means all tools behave consistently and improvements to one tool can benefit all of them.

**Location:** `tools/shared/`

Reusable utilities across all tools:

- **Storage Handler** - Safe localStorage operations
- **Error Handler** - Consistent error handling
- **Validator** - Form validation
- **i18n** - Translations
- **Dark Mode** - Theme management
- **Analytics** - Usage tracking
- **PWA** - Offline support

---

## 10. Social Scraper Recovery Script

**In plain English:** The social media research project processes thousands of videos. This script helps recover and merge data if processing is interrupted, ensuring no work is lost.

> **Note:** This is for an internal research project, not a public tool.

**Location:** `social-scraper/scripts/merge_recovery.py`

Automated script to merge recovery batch data:

- **Validates** recovery data integrity
- **Creates backups** before merging
- **Updates checkpoints** with correct totals
- **Generates reports** of merge operations

### Usage
```bash
python scripts/merge_recovery.py
```

---

## Implementation Notes

### For HTML Tools

Each HTML tool is a self-contained single file. To integrate the shared utilities:

1. Include the utility code inline (after babel compilation)
2. Or use a build step to bundle the utilities
3. Initialize utilities in the main React component

### For React Apps (LLM Advisor)

Import utilities directly as ES modules:

```javascript
import { createErrorHandler } from '../shared/utils/errorHandling';
import { createStorageHandler } from '../shared/utils/storage';
```

### For Python (Social Scraper)

Use the pytest infrastructure for testing:

```bash
pytest tests/ -v --cov=.
```

---

## Next Steps

1. **Apply error handling** to each HTML tool individually
2. **Add more test coverage** (target 70%+)
3. **Generate PWA icons** for all required sizes
4. **Set up Netlify/Vercel** for automatic deployments
5. **Configure Plausible** analytics account
6. **Create component library** build pipeline

---

## Files Added/Modified

### New Files
- `tools/shared/utils/*.js` - Utility functions
- `tools/shared/locales/*.json` - Translations
- `tools/manifest.json` - PWA manifest
- `tools/sw.js` - Service worker
- `.github/workflows/ci.yml` - CI/CD pipeline
- `tools/llm-advisor/src/__tests__/*.js` - React tests
- `social-scraper/tests/*.py` - Python tests
- `social-scraper/pytest.ini` - pytest config
- `social-scraper/scripts/merge_recovery.py` - Recovery merge script

### Documentation
- `tools/shared/README.md` - Shared utilities documentation
- `ENHANCEMENTS.md` - This document

---

## License

MIT License - Center for Cooperative Media
