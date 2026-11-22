// ESLint for the two Tauri + Svelte 5 apps and their shared front-end.
//   npm run lint   (repo root; also runs in pre-commit and CI)
import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';

const APPS = ['Nomoscope-agentic-workflow/{ui,rag-ui}/src', 'Nomoscope-agentic-workflow/shared'];

export default [
  {
    ignores: ['**/node_modules/', '**/dist/', '**/src-tauri/', '**/target/', '**/.venv*/', '.claude/', '.scratch/'],
  },
  js.configs.recommended,
  ...svelte.configs['flat/recommended'],
  {
    files: APPS.flatMap((dir) => [`${dir}/**/*.js`, `${dir}/**/*.svelte`]),
    languageOptions: { globals: { ...globals.browser } },
  },
  {
    // node --test suites and build configs
    files: ['**/*.test.js', '**/vite.config.js', '**/svelte.config.js', 'eslint.config.js'],
    languageOptions: { globals: { ...globals.node } },
  },
  {
    rules: {
      // A key must be unique or Svelte 5 throws at runtime: add them one by one
      // where identity matters, not by blanket rule (43 index-keyed lists today).
      'svelte/require-each-key': 'off',
      // Flags every Map/Set, including the throwaway ones built inside $derived.
      'svelte/prefer-svelte-reactivity': 'off',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_', varsIgnorePattern: '^_', caughtErrors: 'none' }],
    },
  },
];
