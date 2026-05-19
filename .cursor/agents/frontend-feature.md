# Agent: Frontend Feature Builder — CareerOS Campus AI

## Trigger
Use when: implementing a new pane, component, or UI feature in apps/web/.

## Always include
- `.cursor/context/frontend-context.md`
- `.obsidian-ai-memory/05-ARCHITECTURE/frontend-ux.md`
- `.obsidian-ai-memory/02-PROJECTS/active-goals.md`

## Execution steps

1. **Read frontend-ux.md** — check navigation model and component map before adding anything
2. **Check active-goals.md** — confirm UI feature is in current week scope
3. **API layer first** — add typed wrapper to `lib/api.ts` before building the component
4. **Types first** — add new types to `components/panes/types.ts` before using them
5. **Hook state** — add state + handler to `useCareerOSWorkspace.ts`
6. **Component** — implement using `CardSection` / `FormField` / `MetricTile` primitives
7. **Styles** — CSS classes in `globals.css`, not inline styles
8. **Wire** — pass new props through `page.tsx` → pane component
9. **Verify**: `pnpm exec tsc --noEmit` from `apps/web/`
10. **Write session digest** → commit vault

## Checklist before "done"

- [ ] No `fetch()` inline — all HTTP via `lib/api.ts`
- [ ] `"use client"` only where strictly needed
- [ ] No Tailwind, no inline styles for reusable patterns
- [ ] Buttons have `type="button"` or `type="submit"`
- [ ] File inputs have `id` + `<label htmlFor>` or `aria-label`
- [ ] Form fields use `FormField` with a real `<label>`
- [ ] `tsc --noEmit` passes
- [ ] No `any` types
