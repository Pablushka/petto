# Copilot Instructions for Doko

## Project Overview

- **Doko** is a Progressive Web App for reuniting lost pets with owners.
- **Backend:** Python 3, FastAPI, SQLite (default, scalable to MySQL/PostgreSQL)
- **Frontend:** SvelteKit 5, Tailwind CSS, Prisma ORM, Paraglide for i18n.

## Architecture & Data Flow

- **Backend** exposes REST endpoints via FastAPI (`backend/main.py`).
  - Routers are modular: `backend/routers/` (users, pets, banners, qrcode, pet_location, static).
  - Models are in `backend/models.py` (User, Pet, Location, etc.).
  - Database config: `backend/database.py` (SQLite by default).
  - Health check: `GET /_health`.
- **Frontend** is a SvelteKit SPA (`frontend/`).
  - Main routes in `frontend/src/routes/`.
  - i18n via Paraglide: messages in `frontend/src/lib/paraglide/messages/`.
  - Paraglide messages are auto-generated JS exports (see `messages/_index.js`).
  - Tailwind for styling; see `app.css` and config files.

## Developer Workflows

- **Backend:**
  - Start: `uvicorn main:app --reload` (from `backend/`)
  - Dependencies: `pip install -r requirements.txt` (or manual install)
  - API docs: `/docs` when running
- **Frontend:**
  - Install: `pnpm install` (or npm/yarn)
  - Dev server: `pnpm run dev` (or npm run dev)
  - Build: `pnpm run build`
  - Preview: `pnpm run preview`
  - Unit tests: `pnpm run test:unit` (Vitest)
  - E2E tests: `pnpm run test:e2e` (Playwright)
  - Lint/format: `pnpm run lint`, `pnpm run format`
  - SvelteKit sync: `pnpm run prepare`

## Project-Specific Patterns

- **Routers:** Each API feature is a separate router module, imported in `main.py`.
- **Models:** Use Tortoise ORM models; see `models.py` for conventions.
- **Frontend i18n:**
  - Paraglide messages are imported as named exports (e.g., `import { m } from '$lib/paraglide/messages'`).
  - Each message (e.g., `button_cancel`) is a function, not a string. Call with `m.button_cancel()`.
  - Locale switching: `setLocale('en')`, etc. Messages update reactively if used via Svelte stores.
- **Testing:**
  - Unit tests: `src/demo.spec.ts`, `page.svelte.spec.ts` (Vitest)
  - E2E: `e2e/demo.test.ts` (Playwright)

## Integration Points

- **Paraglide:** For i18n, messages are auto-generated and must be called as functions.
- **Prisma ORM:** Used for frontend data modeling (see config files).
- **API:** Frontend communicates with backend via REST endpoints.

## Conventions & Gotchas

- **Do not** access Paraglide messages as properties; always call as functions.
- **Router modules** must be registered in `main.py` to be active.
- **Database migrations** are manual; update models and migrate as needed.
- **Frontend uses SvelteKit 5**; check `svelte.config.js` for adapter info.
- **Tailwind** is configured via `app.css` and plugin configs.

## Key Files & Directories

- `backend/main.py`, `backend/routers/`, `backend/models.py`, `backend/database.py`
- `frontend/src/routes/`, `frontend/src/lib/paraglide/messages/`, `frontend/app.css`, `frontend/package.json`

---

For unclear conventions or missing info, ask the user for clarification or examples from the codebase.

For Sveltekit documentations, refer to the official SvelteKit documentation at https://svelte.dev/llms-small.txt
