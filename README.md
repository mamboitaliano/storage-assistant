# Storage Assistant

A Home Assistant add-on to make managing your home storage just a little bit eaiser.

FastAPI + SQLite backend with a React/Vite frontend for managing floors, rooms, containers, and items. Includes seeded dev data, shadcn/ui components, and feature-scoped tables built on TanStack React Table.

## Prerequisites
- Python 3.12+ (backend) with `venv`
- Node 18+ (frontend)

## Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run API
python -m uvicorn app.main:app --reload --app-dir .
```

- API served at `http://127.0.0.1:8000` (docs at `/docs`).
- SQLite DB lives at `${DATA_DIR:-/data}/storage.db`. Set `DATA_DIR` to override.
- Foreign-key cascades require SQLite PRAGMA `foreign_keys=ON` (enabled in app startup).

### Seeding data
```bash
cd backend
source venv/bin/activate
python -m app.seed.runner
```
This wipes existing data and seeds floors → rooms → containers → items with Faker data. Remove the delete block in `app/seed/runner.py` if you don’t want a full reset.

## Frontend
```bash
cd frontend
npm install
npm run dev
```

- Vite dev server on `http://127.0.0.1:5173` proxied to the backend for `/api` and `/static`.
- Tailwind v3 with shadcn/ui primitives (`src/components/ui/*`) and feature-specific tables under `src/features/*`.
- Path alias: `@` → `src` (configured in `tsconfig.app.json` and `vite.config.ts`).

## Useful paths
- Backend app: `backend/app`
- Routers/services/schemas: `backend/app/routers`, `backend/app/services`, `backend/app/schemas`
- Seeders: `backend/app/seed`
- Frontend pages: `frontend/src/pages`
- Feature tables & columns: `frontend/src/features/*`
- UI primitives: `frontend/src/components/ui`

## Common commands
- Run backend: `python -m uvicorn app.main:app --reload --app-dir backend`
- Seed DB: `python -m app.seed.runner`
- Run frontend: `npm run dev` (from `frontend`)
- Lint frontend: `npm run lint`
