# CCM Shared Utilities

Shared components, utilities, and infrastructure for all CCM journalism tools.

## Overview

This directory contains reusable code that can be integrated into any of the CCM browser-based tools to provide:

- **Error Handling** - Consistent error handling and user notifications
- **Storage** - Safe localStorage operations with quota management
- **Validation** - Form validation and input sanitization
- **Internationalization** - Multi-language support (English/Spanish)
- **Dark Mode** - Theme switching with system preference detection
- **Analytics** - Privacy-preserving usage tracking
- **PWA Support** - Offline functionality and install prompts

## Directory Structure

```
shared/
├── components/       # Reusable React components
├── locales/          # Translation files
│   ├── en.json       # English translations
│   └── es.json       # Spanish translations
├── tests/            # Shared test utilities
└── utils/            # Utility functions
    ├── analytics.js  # Privacy-preserving analytics
    ├── darkMode.js   # Dark mode toggle
    ├── errorHandling.js  # Error handling utilities
    ├── i18n.js       # Internationalization
    ├── pwa.js        # PWA utilities
    ├── storage.js    # localStorage wrapper
    └── validation.js # Form validation
```

## Usage

### Error Handling

```javascript
// In your React component
const { wrapAsync, exportPDF } = createErrorHandler(showToast);

// Wrap async operations
const handleSave = () => wrapAsync(
  async () => {
    await saveData();
  },
  {
    successMessage: 'Saved successfully',
    errorMessage: 'Failed to save. Please try again.'
  }
);

// Export PDF with error handling
const handleExport = () => exportPDF(
  document.getElementById('printable'),
  { filename: 'report.pdf' }
);
```

### Storage

```javascript
const storage = createStorageHandler('myTool', showToast);

// Save data
storage.save('settings', { theme: 'dark' });

// Load data with default
const settings = storage.load('settings', { theme: 'light' });

// Check quota
const { usedFormatted } = storage.getUsage();
console.log(`Using ${usedFormatted} of storage`);
```

### Validation

```javascript
const validator = createValidator();

// Validate form
const result = validator.combine([
  validator.required(name, 'Name'),
  validator.positiveNumber(amount, 'Amount'),
  validator.email(email)
]);

if (!result.isValid) {
  result.errors.forEach(err => showToast(err, 'error'));
}
```

### Internationalization

```javascript
// Load translations
const i18n = createI18n('en');

// Use in component
const label = i18n.t('common.save'); // "Save"
const error = i18n.t('validation.required', { field: 'Name' }); // "Name is required"

// Switch language
i18n.setLocale('es');
```

### Dark Mode

```javascript
const darkMode = createDarkModeHandler();

// Initialize on app load
darkMode.init();

// Toggle
const isDark = darkMode.toggle();

// Check state
if (darkMode.isDark()) {
  // Apply dark styles
}
```

### Analytics

```javascript
const analytics = createAnalytics({ enabled: true });

// Track events
analytics.trackToolUsage('Invoicer', 'generate');
analytics.trackExport('Budget Calculator', 'PDF');

// No personal data is collected
```

### PWA

```javascript
const pwa = createPWAHandler({
  onUpdateFound: () => showToast('Update available'),
  onInstallPrompt: (available) => setShowInstall(available)
});

// Register service worker
await pwa.register();

// Show install prompt
if (pwa.canInstall()) {
  await pwa.showInstallPrompt();
}
```

## Integration

To integrate these utilities into an HTML-based tool:

1. Include the utility scripts via a build step or inline
2. Initialize the utilities in your React component
3. Use the provided patterns for error handling, storage, etc.

For modular React apps (like LLM Advisor), import directly:

```javascript
import { createErrorHandler } from '../shared/utils/errorHandling';
import { createStorageHandler } from '../shared/utils/storage';
```

## Testing

Run tests with:

```bash
# For React apps
npm test

# For utilities
npm run test:utils
```

## Contributing

1. Keep utilities pure and side-effect free where possible
2. Always include JSDoc comments
3. Provide both ES module and inline script versions
4. Test with multiple browsers (Chrome, Firefox, Safari)

## License

MIT License - Center for Cooperative Media
