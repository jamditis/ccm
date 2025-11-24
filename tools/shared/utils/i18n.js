/**
 * Internationalization (i18n) utilities for CCM tools
 *
 * Lightweight i18n solution for browser-based tools.
 * Supports English and Spanish with template interpolation.
 */

import en from '../locales/en.json';
import es from '../locales/es.json';

const translations = { en, es };

/**
 * Create an i18n handler
 * @param {string} initialLocale - Initial locale (default: 'en')
 * @returns {Object} i18n utilities
 */
export function createI18n(initialLocale = 'en') {
  let currentLocale = initialLocale;

  return {
    /**
     * Get the current locale
     * @returns {string} Current locale code
     */
    getLocale() {
      return currentLocale;
    },

    /**
     * Set the current locale
     * @param {string} locale - Locale code ('en' or 'es')
     */
    setLocale(locale) {
      if (translations[locale]) {
        currentLocale = locale;
        // Store preference
        try {
          localStorage.setItem('ccm_locale', locale);
        } catch (e) {
          // Ignore storage errors
        }
      }
    },

    /**
     * Translate a key with optional interpolation
     * @param {string} key - Dot-notation key (e.g., 'common.save')
     * @param {Object} params - Parameters for interpolation
     * @returns {string} Translated string
     */
    t(key, params = {}) {
      const keys = key.split('.');
      let value = translations[currentLocale];

      for (const k of keys) {
        if (value && typeof value === 'object') {
          value = value[k];
        } else {
          value = undefined;
          break;
        }
      }

      // Fallback to English if not found
      if (value === undefined) {
        value = translations.en;
        for (const k of keys) {
          if (value && typeof value === 'object') {
            value = value[k];
          } else {
            value = key; // Return the key itself as last resort
            break;
          }
        }
      }

      // Interpolate parameters
      if (typeof value === 'string' && Object.keys(params).length > 0) {
        Object.entries(params).forEach(([param, val]) => {
          value = value.replace(new RegExp(`{{${param}}}`, 'g'), val);
        });
      }

      return value || key;
    },

    /**
     * Get available locales
     * @returns {Array} Array of locale objects
     */
    getAvailableLocales() {
      return [
        { code: 'en', name: 'English', flag: '🇺🇸' },
        { code: 'es', name: 'Español', flag: '🇪🇸' }
      ];
    },

    /**
     * Detect browser locale
     * @returns {string} Detected locale code
     */
    detectLocale() {
      // Check stored preference first
      try {
        const stored = localStorage.getItem('ccm_locale');
        if (stored && translations[stored]) {
          return stored;
        }
      } catch (e) {
        // Ignore storage errors
      }

      // Check browser language
      const browserLang = navigator.language || navigator.userLanguage;
      if (browserLang) {
        const langCode = browserLang.split('-')[0].toLowerCase();
        if (translations[langCode]) {
          return langCode;
        }
      }

      return 'en';
    }
  };
}

/**
 * React hook for i18n (to be used in components)
 */
export const useI18nCode = `
function useI18n() {
  const [locale, setLocale] = React.useState('en');
  const i18n = React.useMemo(() => createI18n(locale), [locale]);

  React.useEffect(() => {
    const detected = i18n.detectLocale();
    setLocale(detected);
  }, []);

  const changeLocale = (newLocale) => {
    i18n.setLocale(newLocale);
    setLocale(newLocale);
  };

  return { t: i18n.t.bind(i18n), locale, changeLocale, locales: i18n.getAvailableLocales() };
}
`;

/**
 * Language selector component code
 */
export const LanguageSelectorCode = `
const LanguageSelector = ({ locale, onChange, locales }) => (
  <select
    value={locale}
    onChange={(e) => onChange(e.target.value)}
    className="text-xs bg-transparent border border-gray-300 rounded px-2 py-1"
  >
    {locales.map(l => (
      <option key={l.code} value={l.code}>{l.flag} {l.name}</option>
    ))}
  </select>
);
`;

// Export translations for direct use
export { translations };
