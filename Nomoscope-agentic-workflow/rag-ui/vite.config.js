import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// 5174, not the review UI's 5173: both apps can run side by side.
export default defineConfig({
  plugins: [svelte()],
  clearScreen: false,
  server: { port: 5174, strictPort: true },
  build: { target: 'es2021' },
});
