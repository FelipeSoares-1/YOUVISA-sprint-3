import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Expose to all IPs (0.0.0.0)
    port: 5173,  // Fixed port
    strictPort: true, // Fail if port is busy
  }
})
