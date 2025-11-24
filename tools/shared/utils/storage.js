/**
 * Storage utilities for CCM tools
 *
 * Provides safe localStorage operations with error handling,
 * quota management, and data migration support.
 */

/**
 * Create a storage handler with error handling
 * @param {string} prefix - Storage key prefix for namespacing
 * @param {Function} showToast - Optional toast notification function
 * @returns {Object} Storage utilities
 */
export function createStorageHandler(prefix, showToast = null) {
  const notify = (message, type) => {
    if (showToast) {
      showToast(message, type);
    }
  };

  return {
    /**
     * Save data to localStorage
     * @param {string} key - Storage key
     * @param {*} data - Data to save (will be JSON serialized)
     * @returns {boolean} Success status
     */
    save(key, data) {
      const fullKey = `${prefix}_${key}`;

      try {
        const serialized = JSON.stringify(data);
        localStorage.setItem(fullKey, serialized);
        return true;
      } catch (error) {
        console.error('Storage save failed:', error);

        if (error.name === 'QuotaExceededError') {
          notify('Storage is full. Please clear some saved data.', 'error');
        } else {
          notify('Failed to save data', 'error');
        }

        return false;
      }
    },

    /**
     * Load data from localStorage
     * @param {string} key - Storage key
     * @param {*} defaultValue - Default value if key doesn't exist
     * @returns {*} Loaded data or default value
     */
    load(key, defaultValue = null) {
      const fullKey = `${prefix}_${key}`;

      try {
        const serialized = localStorage.getItem(fullKey);

        if (serialized === null) {
          return defaultValue;
        }

        return JSON.parse(serialized);
      } catch (error) {
        console.error('Storage load failed:', error);

        // If JSON parsing fails, the data might be corrupted
        if (error instanceof SyntaxError) {
          console.warn('Corrupted data detected, clearing key:', fullKey);
          localStorage.removeItem(fullKey);
        }

        return defaultValue;
      }
    },

    /**
     * Remove data from localStorage
     * @param {string} key - Storage key
     * @returns {boolean} Success status
     */
    remove(key) {
      const fullKey = `${prefix}_${key}`;

      try {
        localStorage.removeItem(fullKey);
        return true;
      } catch (error) {
        console.error('Storage remove failed:', error);
        return false;
      }
    },

    /**
     * Check if storage is available
     * @returns {boolean} Availability status
     */
    isAvailable() {
      try {
        const testKey = '__storage_test__';
        localStorage.setItem(testKey, 'test');
        localStorage.removeItem(testKey);
        return true;
      } catch (error) {
        return false;
      }
    },

    /**
     * Get all keys for this prefix
     * @returns {string[]} Array of keys
     */
    getKeys() {
      const keys = [];
      const prefixWithUnderscore = `${prefix}_`;

      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith(prefixWithUnderscore)) {
          keys.push(key.substring(prefixWithUnderscore.length));
        }
      }

      return keys;
    },

    /**
     * Clear all data for this prefix
     * @returns {boolean} Success status
     */
    clearAll() {
      try {
        const keys = this.getKeys();
        keys.forEach(key => this.remove(key));
        return true;
      } catch (error) {
        console.error('Storage clearAll failed:', error);
        return false;
      }
    },

    /**
     * Get storage usage information
     * @returns {Object} Usage info with used bytes and quota
     */
    getUsage() {
      try {
        let totalSize = 0;
        const prefixWithUnderscore = `${prefix}_`;

        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key && key.startsWith(prefixWithUnderscore)) {
            const value = localStorage.getItem(key);
            totalSize += key.length + (value ? value.length : 0);
          }
        }

        // Convert to bytes (UTF-16 uses 2 bytes per character)
        return {
          used: totalSize * 2,
          usedFormatted: formatBytes(totalSize * 2)
        };
      } catch (error) {
        return { used: 0, usedFormatted: '0 B' };
      }
    }
  };
}

/**
 * Format bytes to human readable string
 * @param {number} bytes - Number of bytes
 * @returns {string} Formatted string
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Auto-save hook for React
 * Usage: useAutoSave(data, storageKey, delay)
 */
export const useAutoSaveCode = `
function useAutoSave(data, storageKey, delay = 1000, storage) {
  const timeoutRef = React.useRef(null);

  React.useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      storage.save(storageKey, data);
    }, delay);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [data, storageKey, delay]);
}
`;
