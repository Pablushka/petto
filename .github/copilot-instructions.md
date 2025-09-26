# Copilot Instructions for Petto

## Project Overview

- **Petto** is a Progressive Web App for reuniting lost pets with owners.
- **Backend:** Python 3, FastAPI, SQLite (default, scalable to MySQL/PostgreSQL)
- **Frontend:** SvelteKit 5, Tailwind CSS, Prisma ORM, Paraglide for i18n.

## Backend API Endpoints

- Health: `GET /_health` — returns `{ status: "ok" }`
- Users:
  - `POST /api/register` — register new user
  - `POST /api/password-recovery` — request password recovery
  - `POST /api/password-reset` — reset password with token
- Pets:
  - `POST /api/pets/` — create pet
  - `GET /api/pets/` — list pets for current user
  - `GET /api/pets/{pet_id}` — get pet by ID
  - `PUT /api/pets/{pet_id}` — update pet
  - `DELETE /api/pets/{pet_id}` — delete pet
- Banners: `GET /api/banners/{pet_id}` — generate lost pet banner PNG
- QR Code:
  - `GET /api/qrcode/{pet_id}` — generate QR code PNG
  - `POST /api/qrcode/scan/{scan_id}` — record QR scan
- Pet Location & QR:
  - `POST /api/pet-location/scan` — record pet scan event
  - `GET /api/pet-location/pet/{pet_id}/qr-link` — get QR link for pet
  - `GET /api/pet-location/pet/{pet_id}/scans` — get scan events for pet
- Static: `GET /static/{filename}` — serve static files
- Templates: `GET /` (home), `GET /{page_name}` (render HTML from templates)

## Architecture & Data Flow

- **Backend** exposes REST endpoints via FastAPI (`backend/main.py`).
  - Routers are modular: `backend/routers/` (users, pets, banners, qrcode, pet_location, static).
  - Models are in `backend/models.py` (User, Pet, Location, etc.).
  - Database config: `backend/database.py` (SQLite by default).
  - Health check: `GET /_health`.
- **Frontend** is a SvelteKit SPA (`frontend/`).
  - Main routes in `frontend/src/routes/`.
  - i18n using Paraglide: messages in `frontend/src/lib/paraglide/messages/`.
  - Paraglide messages are auto-generated JS exports (see `messages/_index.js`).
  - Tailwind for styling; see `app.css` and config files.
  - Svelte 5 for UI components and routing.
  - Avoid Svelte 4.

## Project-Specific Patterns

- **Routers:** Each API feature is a separate router module, imported in `main.py`.
- **Models:** Use Tortoise ORM models; see `models.py` for conventions.
- **Frontend i18n:**
  - Paraglide messages are imported as named exports (e.g., `import { m } from '$lib/paraglide/messages'`).
  - Each message (e.g., `button_cancel`) is a function, not a string. Call with `m.button_cancel()`.
  - Locale switching: `setLocale('en')`, etc. Messages update reactively if used via Svelte stores.

## Integration Points

- **Paraglide:** For i18n, messages are auto-generated and must be called as functions.
- **Prisma ORM:** Used for frontend data modeling (see config files).

## Conventions & Gotchas

- **Do not** access Paraglide messages as properties; always call as functions.
- **Router modules** must be registered in `main.py` to be active.
- **Database migrations** are manual; update models and migrate as needed.
- **Backend:** Use Tortoise's pydantic_model_creator for API responses; avoid from_queryset for lists, use list comprehension with from_tortoise_orm instead.
- **Frontend uses SvelteKit 5**; check `svelte.config.js` for adapter info.
- **Tailwind** is configured via `app.css` and plugin configs.

## IMPORTANT

For unclear conventions or missing info, ask the user for clarification or take examples from the codebase.

For Sveltekit documentations, refer to the official SvelteKit documentation at https://svelte.dev/llms-small.txt

For tailwind documentation, refer to the official Tailwind CSS documentation at tailwind-llm.txt in this project.
