import { expect, test } from '@playwright/test';

test('home lists the items the API returns, in the same order', async ({ page, request }) => {
  const items = (await (await request.get('/api/items')).json()) as { name: string }[];
  await page.goto('/');
  await expect(page.getByRole('listitem')).toHaveText(items.map((i) => i.name));
});
