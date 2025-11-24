/**
 * Validation utilities for CCM tools
 *
 * Provides form validation, input sanitization, and error messaging
 * for financial and other data-entry tools.
 */

/**
 * Create a validator for form data
 * @returns {Object} Validation utilities
 */
export function createValidator() {
  return {
    /**
     * Validate a required field
     * @param {*} value - Value to check
     * @param {string} fieldName - Field name for error message
     * @returns {Object} Validation result
     */
    required(value, fieldName) {
      const isValid = value !== null && value !== undefined && value !== '';
      return {
        isValid,
        error: isValid ? null : `${fieldName} is required`
      };
    },

    /**
     * Validate a positive number
     * @param {number} value - Value to check
     * @param {string} fieldName - Field name for error message
     * @returns {Object} Validation result
     */
    positiveNumber(value, fieldName) {
      const num = parseFloat(value);
      const isValid = !isNaN(num) && num >= 0;
      return {
        isValid,
        error: isValid ? null : `${fieldName} must be a positive number`
      };
    },

    /**
     * Validate a number within a range
     * @param {number} value - Value to check
     * @param {number} min - Minimum value
     * @param {number} max - Maximum value
     * @param {string} fieldName - Field name for error message
     * @returns {Object} Validation result
     */
    numberInRange(value, min, max, fieldName) {
      const num = parseFloat(value);
      const isValid = !isNaN(num) && num >= min && num <= max;
      return {
        isValid,
        error: isValid ? null : `${fieldName} must be between ${min} and ${max}`
      };
    },

    /**
     * Validate currency amount
     * @param {number} value - Value to check
     * @param {string} fieldName - Field name for error message
     * @returns {Object} Validation result
     */
    currency(value, fieldName) {
      const num = parseFloat(value);
      const isValid = !isNaN(num) && num >= 0 && Number.isFinite(num);
      return {
        isValid,
        error: isValid ? null : `${fieldName} must be a valid currency amount`
      };
    },

    /**
     * Validate email format
     * @param {string} value - Email to check
     * @param {string} fieldName - Field name for error message
     * @returns {Object} Validation result
     */
    email(value, fieldName = 'Email') {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      const isValid = !value || emailRegex.test(value);
      return {
        isValid,
        error: isValid ? null : `${fieldName} must be a valid email address`
      };
    },

    /**
     * Validate phone number format
     * @param {string} value - Phone to check
     * @param {string} fieldName - Field name for error message
     * @returns {Object} Validation result
     */
    phone(value, fieldName = 'Phone') {
      const phoneRegex = /^[\d\s\-\+\(\)]+$/;
      const isValid = !value || phoneRegex.test(value);
      return {
        isValid,
        error: isValid ? null : `${fieldName} must be a valid phone number`
      };
    },

    /**
     * Validate text length
     * @param {string} value - Text to check
     * @param {number} minLength - Minimum length
     * @param {number} maxLength - Maximum length
     * @param {string} fieldName - Field name for error message
     * @returns {Object} Validation result
     */
    textLength(value, minLength, maxLength, fieldName) {
      const length = (value || '').length;
      const isValid = length >= minLength && length <= maxLength;
      return {
        isValid,
        error: isValid ? null : `${fieldName} must be between ${minLength} and ${maxLength} characters`
      };
    },

    /**
     * Validate that budget expenses don't exceed revenue
     * @param {number} expenses - Total expenses
     * @param {number} revenue - Total revenue
     * @returns {Object} Validation result
     */
    budgetBalance(expenses, revenue) {
      const isValid = revenue >= expenses;
      return {
        isValid,
        error: isValid ? null : `Expenses ($${expenses.toFixed(2)}) exceed revenue ($${revenue.toFixed(2)})`
      };
    },

    /**
     * Run multiple validations and collect errors
     * @param {Array} validations - Array of validation results
     * @returns {Object} Combined validation result
     */
    combine(validations) {
      const errors = validations
        .filter(v => !v.isValid)
        .map(v => v.error);

      return {
        isValid: errors.length === 0,
        errors
      };
    }
  };
}

/**
 * Input sanitization functions
 */
export const sanitize = {
  /**
   * Sanitize text input (remove leading/trailing whitespace)
   * @param {string} value - Input value
   * @returns {string} Sanitized value
   */
  text(value) {
    return (value || '').trim();
  },

  /**
   * Sanitize number input
   * @param {*} value - Input value
   * @param {number} defaultValue - Default if invalid
   * @returns {number} Sanitized number
   */
  number(value, defaultValue = 0) {
    const num = parseFloat(value);
    return isNaN(num) ? defaultValue : num;
  },

  /**
   * Sanitize currency input (round to 2 decimal places)
   * @param {*} value - Input value
   * @param {number} defaultValue - Default if invalid
   * @returns {number} Sanitized currency amount
   */
  currency(value, defaultValue = 0) {
    const num = parseFloat(value);
    return isNaN(num) ? defaultValue : Math.round(num * 100) / 100;
  },

  /**
   * Sanitize integer input
   * @param {*} value - Input value
   * @param {number} defaultValue - Default if invalid
   * @returns {number} Sanitized integer
   */
  integer(value, defaultValue = 0) {
    const num = parseInt(value, 10);
    return isNaN(num) ? defaultValue : num;
  }
};

/**
 * Validation error display component code
 */
export const ValidationErrorCode = `
const ValidationError = ({ error }) => {
  if (!error) return null;

  return (
    <div className="text-xs text-red-600 mt-1 flex items-center gap-1">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      {error}
    </div>
  );
};
`;
