import { defineConfig } from 'vitest/config';

export default defineConfig({
  // Web's `@/` alias, so a test can import a module that uses it.
  resolve: { alias: { '@': `${import.meta.dirname}/apps/web/src` } },
  test: {
    include: ['{apps,packages}/*/src/**/*.test.{ts,tsx}'],
    coverage: {
      provider: 'v8',
      include: ['{apps,packages}/*/src/**/*.{ts,tsx}'],
      exclude: ['**/routeTree.gen.ts', '**/components/ui/**'],
      reporter: ['text'],
    },
  },
});
