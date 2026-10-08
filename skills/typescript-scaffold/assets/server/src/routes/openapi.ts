import { resolver } from 'hono-openapi';

/** A `describeRoute` response whose JSON body is `schema`. */
export const jsonResponse = (schema: Parameters<typeof resolver>[0], description: string) => ({
  description,
  content: { 'application/json': { schema: resolver(schema) } },
});
