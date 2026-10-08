import { z } from 'zod';

export const Item = z.object({ id: z.number().int(), name: z.string() });
export type Item = z.infer<typeof Item>;
