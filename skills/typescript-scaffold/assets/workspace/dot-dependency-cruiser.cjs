// Import rules. Top to bottom, a layer may import anything below it, never above.
//
// Across packages:
//
//   apps/server, apps/web   Siblings. Server never imports web. Web may import server only
//                           for types (Hono RPC's AppType, erased at build); a runtime import
//                           would bundle server code into the browser.
//   packages/*              Below both apps: a package never imports an app, so it can be
//                           tested and reused without one. Packages may import each other
//                           (cycles are refused) and packages/interface.
//   packages/interface      zod schemas both sides share at runtime. Imports nothing internal,
//                           so either app can be deleted without touching it.
//
// Inside apps/server/src:
//
//   main.ts, app.ts   Entry points: start the process, compose the routes.
//   routes/           HTTP edge: parse the request, call down, shape the response.
//   services/         Logic. No hono here, so it is tested without a request.
//   models/           Data access. The only layer that knows where data lives, so swapping
//                     the mock for a real database touches nothing above it.
//   lib/              Pure helpers. Import nothing internal.
//
// Inside apps/web/src:
//
//   main.tsx          Entry point.
//   routes/           Pages (TanStack file routes).
//   components/       Components shared by pages. A component that imports a page makes the
//                     page impossible to change alone.
//   components/ui/    shadcn primitives. Import only lib/, so `shadcn add` can overwrite them.
//   lib/              Hooks, the API client, pure logic. Tested by vitest without a browser.
//
// A rule for a directory that does not exist yet costs nothing; it applies from the first file.

const SERVER_ENTRY = '^apps/server/src/(main|app)\\.ts$';
const WEB_ENTRY = '^apps/web/src/(main\\.tsx|routeTree\\.gen\\.ts)$';

/** @type {import('dependency-cruiser').IConfiguration} */
module.exports = {
  forbidden: [
    {
      name: 'no-circular',
      severity: 'error',
      from: {},
      to: { circular: true },
    },
    {
      name: 'not-to-unresolvable',
      severity: 'error',
      from: {},
      to: { couldNotResolve: true },
    },
    {
      name: 'packages-not-to-apps',
      comment: 'Every package sits below both apps.',
      severity: 'error',
      from: { path: '^packages/' },
      to: { path: '^apps/' },
    },
    {
      name: 'interface-imports-nothing-internal',
      comment: 'interface is the bottom layer.',
      severity: 'error',
      from: { path: '^packages/interface/' },
      to: { path: '^packages/(?!interface/)' },
    },
    {
      name: 'web-imports-server-types-only',
      comment: 'Runtime imports would bundle server code into the browser.',
      severity: 'error',
      from: { path: '^apps/web/' },
      to: { path: '^apps/server/', dependencyTypesNot: ['type-only'] },
    },
    {
      name: 'server-not-to-web',
      severity: 'error',
      from: { path: '^apps/server/' },
      to: { path: '^apps/web/' },
    },
    {
      name: 'server-not-to-entry',
      comment: 'Only entry points compose the app.',
      severity: 'error',
      from: { path: '^apps/server/src/', pathNot: [SERVER_ENTRY, '\\.test\\.ts$'] },
      to: { path: SERVER_ENTRY },
    },
    {
      name: 'server-services-not-up',
      severity: 'error',
      from: { path: '^apps/server/src/services/' },
      to: { path: '^apps/server/src/routes/' },
    },
    {
      name: 'server-models-not-up',
      severity: 'error',
      from: { path: '^apps/server/src/models/' },
      to: { path: '^apps/server/src/(routes|services)/' },
    },
    {
      name: 'server-lib-not-up',
      severity: 'error',
      from: { path: '^apps/server/src/lib/' },
      to: { path: '^apps/server/src/(routes|services|models)/' },
    },
    {
      name: 'server-hono-only-at-the-edge',
      comment: 'Below routes/, code takes and returns plain values.',
      severity: 'error',
      from: { path: '^apps/server/src/(services|models|lib)/' },
      to: { path: 'node_modules/(@hono/|hono)' },
    },
    {
      name: 'web-not-to-entry',
      severity: 'error',
      from: { path: '^apps/web/src/', pathNot: WEB_ENTRY },
      to: { path: WEB_ENTRY },
    },
    {
      name: 'web-components-not-to-routes',
      severity: 'error',
      from: { path: '^apps/web/src/components/' },
      to: { path: '^apps/web/src/routes/' },
    },
    {
      name: 'web-ui-imports-lib-only',
      comment: '`shadcn add` overwrites these files.',
      severity: 'error',
      from: { path: '^apps/web/src/components/ui/' },
      to: { path: '^apps/web/src/', pathNot: '^apps/web/src/(components/ui|lib)/' },
    },
    {
      name: 'web-lib-not-up',
      severity: 'error',
      from: { path: '^apps/web/src/lib/' },
      to: { path: '^apps/web/src/(routes|components)/' },
    },
  ],
  options: {
    doNotFollow: { path: 'node_modules' },
    // Build output only. A bare /dist/ would also drop every npm package that resolves into its
    // own dist/, and the rules about them with it.
    exclude: { path: '^(apps|packages)/[^/]+/dist/' },
    // Keep type-only imports in the graph so the web -> server rule can tell them apart.
    tsPreCompilationDeps: true,
    // Resolves web's `@/` alias.
    tsConfig: { fileName: 'tsconfig.depcruise.json' },
    enhancedResolveOptions: {
      exportsFields: ['exports'],
      conditionNames: ['import', 'require', 'node', 'default', 'types'],
    },
  },
};
