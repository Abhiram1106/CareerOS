# Shared frontend layer

Cross-module UI and utilities. During migration, canonical primitives remain at:

- `components/ui/primitives.tsx` — CardSection, FormField, MetricTile
- `components/ui/TiltCard.tsx`, etc.
- `lib/api.ts` — all HTTP
- `app/globals.css` — design tokens

New shared code can land here or under `shared/components/ui/` once imports are updated.
