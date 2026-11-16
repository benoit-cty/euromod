import { fileURLToPath } from 'node:url';
import { defineConfig, searchForWorkspaceRoot } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// The front-end both desktop apps share (styles, shell, icons, labels, the
// api core and the job follower) lives in ../shared, imported as @shared.
const shared = fileURLToPath(new URL('../shared', import.meta.url));

// The review UI on 5173 (the RAG chat uses 5174, so both run side by side).
export default defineConfig({
  plugins: [svelte()],
  resolve: { alias: { '@shared': shared }, dedupe: ['svelte'] },
  clearScreen: false,
  server: {
    port: 5173,
    strictPort: true,
    fs: { allow: [searchForWorkspaceRoot(process.cwd()), shared] },
  },
  build: { target: 'es2021' },
});
