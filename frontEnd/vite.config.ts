import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite'; // <-- ADD THIS LINE

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(), // Now this will work without throwing ReferenceError
  ],
});