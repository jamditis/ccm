/**
 * PWA (Progressive Web App) utilities for CCM tools
 *
 * Provides service worker registration, offline support,
 * and install prompt handling.
 */

/**
 * Create a PWA handler
 * @param {Object} options - PWA configuration
 * @returns {Object} PWA utilities
 */
export function createPWAHandler(options = {}) {
  const {
    swPath = '/sw.js',
    onUpdateFound = null,
    onInstallPrompt = null
  } = options;

  let deferredPrompt = null;

  return {
    /**
     * Register the service worker
     * @returns {Promise} Registration result
     */
    async register() {
      if (!('serviceWorker' in navigator)) {
        console.log('Service Worker not supported');
        return null;
      }

      try {
        const registration = await navigator.serviceWorker.register(swPath);
        console.log('Service Worker registered:', registration.scope);

        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                // New version available
                if (onUpdateFound) {
                  onUpdateFound();
                }
              }
            });
          }
        });

        return registration;
      } catch (error) {
        console.error('Service Worker registration failed:', error);
        return null;
      }
    },

    /**
     * Initialize install prompt capture
     */
    initInstallPrompt() {
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        if (onInstallPrompt) {
          onInstallPrompt(true);
        }
      });

      window.addEventListener('appinstalled', () => {
        deferredPrompt = null;
        if (onInstallPrompt) {
          onInstallPrompt(false);
        }
      });
    },

    /**
     * Show the install prompt
     * @returns {Promise<boolean>} Whether the user accepted
     */
    async showInstallPrompt() {
      if (!deferredPrompt) {
        return false;
      }

      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      deferredPrompt = null;

      return outcome === 'accepted';
    },

    /**
     * Check if the app can be installed
     * @returns {boolean} Whether install prompt is available
     */
    canInstall() {
      return deferredPrompt !== null;
    },

    /**
     * Check if the app is running as a PWA
     * @returns {boolean} Whether running as PWA
     */
    isStandalone() {
      return window.matchMedia('(display-mode: standalone)').matches ||
             window.navigator.standalone === true;
    }
  };
}

/**
 * Service worker template
 */
export const serviceWorkerTemplate = `
const CACHE_NAME = 'ccm-tools-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  // Add tool-specific assets here
];

// Install event - cache assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME)
            .map((key) => caches.delete(key))
      );
    })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Skip external requests
  if (!event.request.url.startsWith(self.location.origin)) return;

  event.respondWith(
    caches.match(event.request).then((cached) => {
      // Cache-first strategy for assets
      if (cached) {
        // Fetch in background to update cache
        fetch(event.request).then((response) => {
          if (response.ok) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, response);
            });
          }
        });
        return cached;
      }

      // Network with cache fallback
      return fetch(event.request).then((response) => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, clone);
          });
        }
        return response;
      });
    })
  );
});
`;

/**
 * Manifest.json template generator
 */
export function generateManifest(options = {}) {
  const {
    name = 'CCM Tools',
    shortName = 'CCM',
    description = 'Center for Cooperative Media journalism tools',
    themeColor = '#1a1a1a',
    backgroundColor = '#ffffff',
    startUrl = '/',
    display = 'standalone'
  } = options;

  return {
    name,
    short_name: shortName,
    description,
    theme_color: themeColor,
    background_color: backgroundColor,
    start_url: startUrl,
    display,
    orientation: 'portrait-primary',
    icons: [
      {
        src: '/icons/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
        purpose: 'any maskable'
      },
      {
        src: '/icons/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'any maskable'
      }
    ]
  };
}

/**
 * React hook for PWA features
 */
export const usePWACode = `
function usePWA() {
  const [canInstall, setCanInstall] = React.useState(false);
  const [updateAvailable, setUpdateAvailable] = React.useState(false);

  const pwa = React.useMemo(() => createPWAHandler({
    onUpdateFound: () => setUpdateAvailable(true),
    onInstallPrompt: (available) => setCanInstall(available)
  }), []);

  React.useEffect(() => {
    pwa.register();
    pwa.initInstallPrompt();
  }, []);

  const install = async () => {
    const accepted = await pwa.showInstallPrompt();
    if (accepted) {
      setCanInstall(false);
    }
  };

  return { canInstall, install, updateAvailable, isStandalone: pwa.isStandalone() };
}
`;
