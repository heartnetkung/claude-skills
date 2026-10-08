import { createRootRoute, Outlet } from '@tanstack/react-router';

export const Route = createRootRoute({ component: Layout });

function Layout() {
  return (
    <div className="min-h-screen bg-muted/40">
      <header className="border-b bg-background">
        <h1 className="px-5 py-3 text-sm font-semibold">{{PROJECT}}</h1>
      </header>
      <main className="p-5">
        <Outlet />
      </main>
    </div>
  );
}
