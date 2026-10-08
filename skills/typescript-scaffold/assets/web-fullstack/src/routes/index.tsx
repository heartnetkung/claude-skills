import { createFileRoute } from '@tanstack/react-router';
import { Button } from '@/components/ui/button';
import { useItems } from '@/lib/queries';

export const Route = createFileRoute('/')({ component: Home });

function Home() {
  const items = useItems();
  return (
    <div className="space-y-4">
      <Button onClick={() => items.refetch()}>Refresh</Button>
      {items.isError && <p role="alert">{items.error.message}</p>}
      <ul className="list-disc pl-5">
        {items.data?.map((item) => (
          <li key={item.id}>{item.name}</li>
        ))}
      </ul>
    </div>
  );
}
