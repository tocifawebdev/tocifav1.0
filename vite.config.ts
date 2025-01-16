import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)), // Alias untuk "src"
    },
  },
  server: {
    proxy: {
      '/login': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/usermanagement': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/vendordata': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/customerdata': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/vendoritem': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/listvendor': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/customeritem': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/moneymanagement': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/locklimitrekening': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/requestpo': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/updaterequestpo': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/vendoritempriceunit': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/datetime': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/selectvendoritem': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/selectvendor': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },
      '/vendorinfo': { 
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      },




    },
  },
  build: {
    assetsInlineLimit: 8192, 
  },
});
