import { Scalar } from '@scalar/hono-api-reference';
import { Hono } from 'hono';
import { logger } from 'hono/logger';
import { describeRoute, openAPIRouteHandler } from 'hono-openapi';
import { z } from 'zod';
import { itemRoutes } from './routes/items.ts';
import { jsonResponse } from './routes/openapi.ts';

const Health = z.object({ status: z.literal('ok') });

const buildApi = () =>
  new Hono()
    .basePath('/api')
    .use(logger())
    .get(
      '/health',
      describeRoute({
        summary: 'Liveness check',
        responses: { 200: jsonResponse(Health, 'Server is up') },
      }),
      (c) => c.json({ status: 'ok' as const }),
    )
    .route('/', itemRoutes());

// Typed client for the web app (hc<AppType>). Docs routes are deliberately not part of it.
export type AppType = ReturnType<typeof buildApi>;

export function createApp(): AppType {
  const app = buildApi();
  app.onError((err, c) => {
    console.error(`[routes] ${c.req.method} ${c.req.path} failed:`, err);
    return c.text('Internal Server Error', 500);
  });
  app.get(
    '/openapi.json',
    openAPIRouteHandler(app, {
      documentation: { info: { title: '{{PROJECT}}', version: '0.1.0' } },
    }),
  );
  app.get('/docs', Scalar({ url: '/api/openapi.json' }));
  return app;
}
