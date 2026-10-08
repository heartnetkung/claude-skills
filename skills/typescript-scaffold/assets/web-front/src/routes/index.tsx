import { createFileRoute } from '@tanstack/react-router';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { clickLabel } from '@/lib/clicks';

export const Route = createFileRoute('/')({ component: Home });

function Home() {
  const [count, setCount] = useState(0);
  return (
    <div className="space-y-4">
      <Button onClick={() => setCount(count + 1)}>Click me</Button>
      <p>{clickLabel(count)}</p>
    </div>
  );
}
