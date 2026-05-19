# Agent: Backend Feature Builder — CareerOS Campus AI

## Trigger
Use when: implementing a new FastAPI endpoint, service, or database change.

## Always include
- `.cursor/context/backend-context.md`
- `.cursor/context/database-context.md` (if schema changes)
- `.obsidian-ai-memory/02-PROJECTS/active-goals.md`
- `.obsidian-ai-memory/03-ERRORS/error-memory.md`

## Execution steps

1. **Read active-goals.md** — confirm task is in current week scope
2. **Read error-memory.md** — check for known bugs in this service area
3. **Check schema** — does this need a migration? If yes, write migration FIRST
4. **Implement** — route handler (slim) → service layer → model/schema
5. **Wire** — update `clients.py` if new downstream call; update `config.py` if new env var
6. **Verify**:
   - `python -c "import ast; ast.parse(open('services/<svc>/app/main.py').read())"` on all touched files
   - If migration: `alembic upgrade head` + `alembic downgrade base` + `alembic upgrade head`
7. **Write session digest** → commit vault

## Checklist before "done"

- [ ] Route handler delegates to service layer (no business logic in route)
- [ ] Pydantic v2 schemas in `schemas/contracts.py`
- [ ] SQLAlchemy 2.0 mapped-column style
- [ ] Migration written and tested if schema changed
- [ ] New env var in `config.py` and `.env.example`
- [ ] `clients.py` updated if new downstream service call
- [ ] All touched Python files AST-parse clean
- [ ] No secrets in any file
