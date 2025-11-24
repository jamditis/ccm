/**
 * Dark mode utilities for CCM tools
 *
 * Provides dark mode toggle functionality with system preference detection
 * and localStorage persistence.
 */

/**
 * Create a dark mode handler
 * @returns {Object} Dark mode utilities
 */
export function createDarkModeHandler() {
  const STORAGE_KEY = 'ccm_dark_mode';

  return {
    /**
     * Get the current dark mode preference
     * @returns {boolean} True if dark mode is enabled
     */
    isDark() {
      try {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored !== null) {
          return stored === 'true';
        }
        // Check system preference
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
      } catch (e) {
        return false;
      }
    },

    /**
     * Set dark mode preference
     * @param {boolean} enabled - Whether dark mode should be enabled
     */
    setDark(enabled) {
      try {
        localStorage.setItem(STORAGE_KEY, String(enabled));
        this.applyTheme(enabled);
      } catch (e) {
        console.error('Failed to save dark mode preference:', e);
      }
    },

    /**
     * Toggle dark mode
     * @returns {boolean} New dark mode state
     */
    toggle() {
      const newState = !this.isDark();
      this.setDark(newState);
      return newState;
    },

    /**
     * Apply the theme to the document
     * @param {boolean} isDark - Whether dark mode is enabled
     */
    applyTheme(isDark) {
      if (isDark) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    },

    /**
     * Initialize dark mode (call on app load)
     */
    init() {
      this.applyTheme(this.isDark());

      // Listen for system preference changes
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      mediaQuery.addEventListener('change', (e) => {
        // Only auto-switch if no user preference is stored
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored === null) {
          this.applyTheme(e.matches);
        }
      });
    }
  };
}

/**
 * React hook for dark mode
 */
export const useDarkModeCode = `
function useDarkMode() {
  const darkMode = React.useMemo(() => createDarkModeHandler(), []);
  const [isDark, setIsDark] = React.useState(false);

  React.useEffect(() => {
    darkMode.init();
    setIsDark(darkMode.isDark());
  }, []);

  const toggle = () => {
    const newState = darkMode.toggle();
    setIsDark(newState);
  };

  return { isDark, toggle };
}
`;

/**
 * Dark mode toggle button component
 */
export const DarkModeToggleCode = `
const DarkModeToggle = ({ isDark, onToggle }) => (
  <button
    onClick={onToggle}
    className="p-2 rounded-lg transition-colors hover:bg-gray-200 dark:hover:bg-gray-700"
    title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
  >
    {isDark ? (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="5"></circle>
        <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"></path>
      </svg>
    ) : (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    )}
  </button>
);
`;

/**
 * Tailwind dark mode class mappings
 */
export const darkModeClasses = {
  // Background colors
  bg: {
    primary: 'bg-white dark:bg-gray-900',
    secondary: 'bg-gray-100 dark:bg-gray-800',
    accent: 'bg-blue-500 dark:bg-blue-600'
  },
  // Text colors
  text: {
    primary: 'text-gray-900 dark:text-white',
    secondary: 'text-gray-600 dark:text-gray-300',
    muted: 'text-gray-400 dark:text-gray-500'
  },
  // Border colors
  border: {
    primary: 'border-gray-200 dark:border-gray-700',
    secondary: 'border-gray-100 dark:border-gray-800'
  }
};
