/**
 * Error handling utilities for CCM tools
 *
 * These utilities provide consistent error handling across all tools,
 * including try/catch wrappers, error notifications, and logging.
 */

/**
 * Create an error handler with toast notification
 * @param {Function} showToast - Toast notification function
 * @returns {Object} Error handling utilities
 */
export function createErrorHandler(showToast) {
  return {
    /**
     * Wrap an async operation with error handling
     * @param {Function} operation - Async operation to perform
     * @param {Object} options - Error handling options
     */
    async wrapAsync(operation, options = {}) {
      const {
        errorMessage = 'An error occurred',
        successMessage = null,
        onError = null,
        onSuccess = null,
        rethrow = false
      } = options;

      try {
        const result = await operation();
        if (successMessage) {
          showToast(successMessage, 'success');
        }
        if (onSuccess) {
          onSuccess(result);
        }
        return result;
      } catch (error) {
        console.error('Operation failed:', error);
        showToast(errorMessage, 'error');
        if (onError) {
          onError(error);
        }
        if (rethrow) {
          throw error;
        }
        return null;
      }
    },

    /**
     * Wrap a sync operation with error handling
     * @param {Function} operation - Sync operation to perform
     * @param {Object} options - Error handling options
     */
    wrapSync(operation, options = {}) {
      const {
        errorMessage = 'An error occurred',
        successMessage = null,
        onError = null,
        onSuccess = null,
        rethrow = false
      } = options;

      try {
        const result = operation();
        if (successMessage) {
          showToast(successMessage, 'success');
        }
        if (onSuccess) {
          onSuccess(result);
        }
        return result;
      } catch (error) {
        console.error('Operation failed:', error);
        showToast(errorMessage, 'error');
        if (onError) {
          onError(error);
        }
        if (rethrow) {
          throw error;
        }
        return null;
      }
    },

    /**
     * Handle PDF export with proper error handling
     * @param {HTMLElement} element - Element to export
     * @param {Object} options - PDF export options
     */
    async exportPDF(element, options = {}) {
      const {
        filename = 'export.pdf',
        onStart = null,
        onComplete = null
      } = options;

      if (!element) {
        showToast('Export element not found', 'error');
        return false;
      }

      if (onStart) onStart();

      try {
        const pdfOptions = {
          margin: 0.5,
          filename,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 2, useCORS: true, logging: false },
          jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
          ...options.pdfOptions
        };

        await window.html2pdf().set(pdfOptions).from(element).save();
        showToast('PDF exported successfully', 'success');
        if (onComplete) onComplete();
        return true;
      } catch (error) {
        console.error('PDF export failed:', error);
        showToast('PDF export failed. Try using Chrome or check your browser settings.', 'error');
        if (onComplete) onComplete();
        return false;
      }
    }
  };
}

/**
 * Global error boundary for React components (to be rendered as JSX)
 * Usage: Wrap your app with <ErrorBoundary>
 */
export const ErrorBoundaryCode = `
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('React Error Boundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
          <div className="bg-white p-8 rounded-lg shadow-lg max-w-md text-center">
            <h2 className="text-xl font-bold text-red-600 mb-4">Something went wrong</h2>
            <p className="text-gray-600 mb-4">
              We're sorry, but something unexpected happened. Please try refreshing the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
`;
