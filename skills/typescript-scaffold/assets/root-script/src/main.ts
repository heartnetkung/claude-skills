import { greeting } from './greeting.ts';

console.log(greeting(process.argv[2] ?? 'world'));
