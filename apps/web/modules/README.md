# Frontend modules (feature-first, flat)

Screens stay in `app/` (Next.js App Router). Each feature module keeps only real files,
with no placeholder subfolders:

- `<feature>Service.ts` — API calls through `lib/api.ts`
- `use<Feature>.ts` — client hooks when needed
- `types.ts` — local contracts when needed

If a feature has no runtime code, its folder should not exist.
