import { defineConfig, devices } from '@playwright/test';

// Drives the real stack: Vite web app -> /api proxy -> Hono server. Starts its own servers on
// their own ports, so it never collides with a running `pnpm dev`.
export default defineConfig({
  testDir: 'tests',
  reporter: 'list',
  fullyParallel: true,
  use: { baseURL: 'http://localhost:3002', trace: 'retain-on-failure' },
  projects: [{ name: 'chromium', use: devices['Desktop Chrome'] }],
  webServer: [
    {
      command: 'pnpm --filter @{{SCOPE}}/server start',
      url: 'http://localhost:8788/api/health',
      cwd: '..',
      env: { PORT: '8788' },
    },
    {
      command: 'pnpm --filter @{{SCOPE}}/web dev --port 3002',
      url: 'http://localhost:3002',
      cwd: '..',
      env: { API_TARGET: 'http://localhost:8788' },
    },
  ],
});
