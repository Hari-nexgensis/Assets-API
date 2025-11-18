import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../staticfiles/react',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: './src/main.jsx',
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/assets': {
        target: 'http://localhost',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
