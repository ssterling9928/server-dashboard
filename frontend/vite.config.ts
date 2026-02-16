import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,  // Important for Codespaces forwarded ports
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // FastAPI inside the SAME container
        changeOrigin: true,
        secure: false
      }
    }
  }
})