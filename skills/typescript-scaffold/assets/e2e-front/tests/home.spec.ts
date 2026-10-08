import { expect, test } from '@playwright/test';

test('the button counts its clicks', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('Not clicked yet')).toBeVisible();
  await page.getByRole('button', { name: 'Click me' }).click();
  await expect(page.getByText('Clicked 1 time')).toBeVisible();
});
