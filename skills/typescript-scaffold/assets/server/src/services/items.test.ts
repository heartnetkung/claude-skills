import { expect, test } from 'vitest';
import { itemsByName } from './items.ts';

test('sorts by name', () => {
  expect(itemsByName().map((i) => i.name)).toEqual(['First item', 'Second item']);
});
