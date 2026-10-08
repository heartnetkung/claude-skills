import { expect, test } from 'vitest';
import { createApp } from './app.ts';

const app = createApp();

test('health answers ok', async () => {
  const res = await app.request('/api/health');
  expect(res.status).toBe(200);
  expect(await res.json()).toEqual({ status: 'ok' });
});

test('items come back sorted by name', async () => {
  const res = await app.request('/api/items');
  expect(await res.json()).toEqual([
    { id: 2, name: 'First item' },
    { id: 1, name: 'Second item' },
  ]);
});

test('the OpenAPI spec lists the routes', async () => {
  const spec = (await (await app.request('/api/openapi.json')).json()) as { paths: object };
  expect(Object.keys(spec.paths).sort()).toEqual(['/api/health', '/api/items']);
});
