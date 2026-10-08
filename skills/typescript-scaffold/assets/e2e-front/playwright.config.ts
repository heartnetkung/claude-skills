import { defineConfig, devices } from '@playwright/test';

// Starts its own Vite server on its own port, so it never collides with a running `pnpm dev`.
export default defineConfig({
  testDir: 'tests',
  reporter: 'list',
  fullyParallel: true,
  use: { baseURL: 'http://localhost:3002', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: devices['Desktop Chrome'] }],
  webServer: {
    command: 'pnpm --filter @{{SCOPE}}/web dev --port 3002',
    url: 'http://localhost:3002',
    cwd: '..',
  },
});
