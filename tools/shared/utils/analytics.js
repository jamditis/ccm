/**
 * Privacy-preserving analytics utilities for CCM tools
 *
 * Uses Plausible Analytics or similar privacy-friendly analytics.
 * No cookies, no personal data collection.
 */

/**
 * Create an analytics handler
 * @param {Object} options - Analytics configuration
 * @returns {Object} Analytics utilities
 */
export function createAnalytics(options = {}) {
  const {
    domain = '',
    enabled = true,
    debug = false
  } = options;

  // Check if Plausible is loaded
  const hasPlausible = () => typeof window !== 'undefined' && window.plausible;

  return {
    /**
     * Track a page view
     * @param {string} url - Optional URL (defaults to current page)
     */
    trackPageView(url) {
      if (!enabled) return;

      if (debug) {
        console.log('[Analytics] Page view:', url || window.location.pathname);
      }

      if (hasPlausible()) {
        window.plausible('pageview', { u: url });
      }
    },

    /**
     * Track a custom event
     * @param {string} eventName - Name of the event
     * @param {Object} props - Event properties
     */
    trackEvent(eventName, props = {}) {
      if (!enabled) return;

      if (debug) {
        console.log('[Analytics] Event:', eventName, props);
      }

      if (hasPlausible()) {
        window.plausible(eventName, { props });
      }
    },

    /**
     * Track tool usage
     * @param {string} toolName - Name of the tool
     * @param {string} action - Action performed
     */
    trackToolUsage(toolName, action) {
      this.trackEvent('Tool Usage', {
        tool: toolName,
        action: action
      });
    },

    /**
     * Track export action
     * @param {string} toolName - Name of the tool
     * @param {string} format - Export format (PDF, PNG, etc.)
     */
    trackExport(toolName, format) {
      this.trackEvent('Export', {
        tool: toolName,
        format: format
      });
    },

    /**
     * Track error (for debugging, no personal data)
     * @param {string} toolName - Name of the tool
     * @param {string} errorType - Type of error
     */
    trackError(toolName, errorType) {
      this.trackEvent('Error', {
        tool: toolName,
        type: errorType
      });
    },

    /**
     * Get the Plausible script tag for embedding
     * @param {string} domain - Domain to track
     * @returns {string} Script tag HTML
     */
    getScriptTag(domain) {
      return `<script defer data-domain="${domain}" src="https://plausible.io/js/script.js"></script>`;
    }
  };
}

/**
 * React hook for analytics
 */
export const useAnalyticsCode = `
function useAnalytics(toolName) {
  const analytics = React.useMemo(() => createAnalytics({ enabled: true }), []);

  React.useEffect(() => {
    analytics.trackPageView();
  }, []);

  const trackAction = (action) => {
    analytics.trackToolUsage(toolName, action);
  };

  const trackExport = (format) => {
    analytics.trackExport(toolName, format);
  };

  return { trackAction, trackExport };
}
`;

/**
 * Privacy notice component
 */
export const PrivacyNoticeCode = `
const PrivacyNotice = () => (
  <div className="text-xs text-gray-400 text-center mt-4">
    This tool uses privacy-friendly analytics. No cookies or personal data are collected.
    <a href="https://plausible.io/privacy-focused-web-analytics" target="_blank" rel="noopener" className="underline ml-1">
      Learn more
    </a>
  </div>
);
`;
