import tailwindcss from '@tailwindcss/vite';
import { tanstackRouter } from '@tanstack/router-plugin/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

export default defineConfig({
  // The router plugin must come before react(); it generates src/routeTree.gen.ts.
  plugins: [tanstackRouter({ target: 'react', autoCodeSplitting: true }), react(), tailwindcss()],
  resolve: {
    alias: { '@': `${import.meta.dirname}/src` },
  },
  server: {
    port: 3001,
    strictPort: true,
    proxy: { '/api': process.env.API_TARGET ?? 'http://localhost:8787' },
  },
});
