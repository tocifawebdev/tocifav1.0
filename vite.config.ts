import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/login': { 
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        secure: false,
      },
      '/usermanagement': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        secure: false,
      },
      '/vendordata': { 
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        secure: false,
      },
      '/customerdata': { 
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
        secure: false,
      },

    },
  },
  build: {
    assetsInlineLimit: 8192, 
  },
});
