import type { Item } from '@{{SCOPE}}/interface';
import { listItems } from '../models/items.ts';

export const itemsByName = (): Item[] =>
  listItems().toSorted((a, b) => a.name.localeCompare(b.name));
