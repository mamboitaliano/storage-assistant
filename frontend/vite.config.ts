import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      '/containers': 'http://127.0.0.1:8000',
      '/rooms': 'http://127.0.0.1:8000',
      '/floors': 'http://127.0.0.1:8000',
      '/items': 'http://127.0.0.1:8000',
      '/static': 'http://127.0.0.1:8000',
    }
  }
})
