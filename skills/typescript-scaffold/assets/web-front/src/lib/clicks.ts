/** What the home page says after `count` clicks. */
export const clickLabel = (count: number) =>
  count === 0 ? 'Not clicked yet' : `Clicked ${count} time${count === 1 ? '' : 's'}`;
