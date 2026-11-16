import { fileURLToPath } from 'node:url';
import { defineConfig, searchForWorkspaceRoot } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// The front-end both desktop apps share (styles, shell, icons, labels, the
// api core and the job follower) lives in ../shared, imported as @shared.
const shared = fileURLToPath(new URL('../shared', import.meta.url));

// 5174, not the review UI's 5173: both apps can run side by side.
export default defineConfig({
  plugins: [svelte()],
  resolve: { alias: { '@shared': shared }, dedupe: ['svelte'] },
  clearScreen: false,
  server: {
    port: 5174,
    strictPort: true,
    fs: { allow: [searchForWorkspaceRoot(process.cwd()), shared] },
  },
  build: { target: 'es2021' },
});
