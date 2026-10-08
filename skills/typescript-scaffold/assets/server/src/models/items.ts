import type { Item } from '@{{SCOPE}}/interface';

// Mock data standing in for a database. A real one replaces this file's body; the exports
// stay, so nothing above models/ changes.
const items: Item[] = [
  { id: 1, name: 'Second item' },
  { id: 2, name: 'First item' },
];

export const listItems = (): Item[] => items;
