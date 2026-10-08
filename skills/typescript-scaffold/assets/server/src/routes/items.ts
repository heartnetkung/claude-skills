import { Item } from '@{{SCOPE}}/interface';
import { Hono } from 'hono';
import { describeRoute } from 'hono-openapi';
import { z } from 'zod';
import { itemsByName } from '../services/items.ts';
import { jsonResponse } from './openapi.ts';

export const itemRoutes = () =>
  new Hono().get(
    '/items',
    describeRoute({
      summary: 'Every item, sorted by name',
      responses: { 200: jsonResponse(z.array(Item), 'The items') },
    }),
    (c) => c.json(itemsByName()),
  );
