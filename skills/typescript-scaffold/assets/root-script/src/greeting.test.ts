import { expect, test } from 'vitest';
import { greeting } from './greeting.ts';

test('greets by name', () => {
  expect(greeting('world')).toBe('Hello, world!');
});
