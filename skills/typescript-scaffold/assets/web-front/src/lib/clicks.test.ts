import { expect, test } from 'vitest';
import { clickLabel } from './clicks';

test('counts clicks, singular and plural', () => {
  expect(clickLabel(0)).toBe('Not clicked yet');
  expect(clickLabel(1)).toBe('Clicked 1 time');
  expect(clickLabel(2)).toBe('Clicked 2 times');
});
