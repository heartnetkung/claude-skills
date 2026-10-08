import { serve } from '@hono/node-server';
import { createApp } from './app.ts';

const port = Number(process.env.PORT ?? 8787);

serve({ fetch: createApp().fetch, port }, (info) => {
  console.log(`server listening on http://localhost:${info.port} (docs: /api/docs)`);
});
