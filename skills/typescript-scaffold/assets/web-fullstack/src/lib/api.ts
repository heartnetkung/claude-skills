import type { AppType } from '@{{SCOPE}}/server';
import { hc } from 'hono/client';

export const api = hc<AppType>('/').api;

/** Awaits a typed request and returns its success body; throws the HTTP status otherwise. */
export async function fetchJson<R extends Response>(
  request: Promise<R>,
): Promise<Awaited<ReturnType<Exclude<R, { ok: false }>['json']>>> {
  const res = await request;
  if (!res.ok) {
    console.error(`[api] ${res.url} answered ${res.status} ${res.statusText}`);
    throw new Error(`${res.status} ${res.statusText}`);
  }
  return res.json();
}
