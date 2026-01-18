# AGENTS.md - Petto Project Guidelines

This file contains conventions, commands, and patterns for agentic coding agents working on the Petto project.

## Project Overview

**Petto** is a Progressive Web App for reuniting lost pets with owners.
- **Backend:** Python 3.13+, FastAPI, SQLite (default), Tortoise ORM, Uvicorn
- **Frontend:** SvelteKit 5, TypeScript, Tailwind CSS v4, Paraglide i18n, Vitest + Playwright
- **Package Management:** pnpm (frontend), uv (backend)
- **Architecture:** Monorepo with modular backend routers and Svelte 5 runes

## Build/Lint/Test Commands

### Root Level Commands
```bash
# Development
pnpm dev              # Start frontend only
pnpm dev:frontend     # Start frontend (SvelteKit)
pnpm dev:backend      # Start backend (FastAPI + Uvicorn)
pnpm dev:all          # Start both concurrently

# Build & Quality
pnpm build           # Build frontend for production
pnpm lint             # Lint all packages (frontend + backend)
pnpm test             # Test all packages
```

### Frontend Commands (apps/frontend/)
```bash
# Development
pnpm dev              # Start SvelteKit dev server
pnpm build           # Build for production
pnpm preview          # Preview production build

# Code Quality
pnpm check            # Svelte type checking + sync
pnpm check:watch      # Type checking with watch mode
pnpm format           # Prettier formatting
pnpm lint             # ESLint + Prettier check
pnpm lint:svelte-runes # Check for Svelte 4 lifecycle usage

# Testing
pnpm test:unit        # Run Vitest unit tests
pnpm test:e2e         # Run Playwright E2E tests
pnpm test             # Run both unit and E2E tests

# Single Test Commands
pnpm test:unit path/to/file.test.ts        # Run specific unit test
pnpm test:e2e path/to/file.spec.ts         # Run specific E2E test
```

### Backend Commands (backend/)
```bash
# Development
uv run uvicorn main:app --reload           # Start FastAPI dev server
uv run python -m autopep8 .               # Format Python code

# Testing (add test commands when implemented)
uv run pytest                             # Run tests (if pytest is added)
```

## Code Style Guidelines

### Frontend (SvelteKit 5 + TypeScript)

#### Svelte 5 Requirements
- **MANDATORY:** Use Svelte 5 runes only - NO Svelte 4 lifecycle imports
- **BANNED:** `onMount`, `beforeUpdate`, `afterUpdate`, `createEventDispatcher`
- **REACTIVE:** Use `$state`, `$effect`, `$derived` instead of `$:` reactive statements
- **PROPS:** Use `$props<{...}>()` syntax for component props
- **CHILDREN:** Use `{@render children?.()}` for slot rendering

#### Component Structure
```typescript
// Correct Svelte 5 component pattern
<script lang="ts">
  let { count = 0 }: { count?: number } = $props();
  
  $effect(() => {
    console.log('Count changed:', count);
  });
  
  const doubled = $derived(count * 2);
</script>

<button onclick={() => count++}>{doubled}</button>
```

#### TypeScript Conventions
- **STRICT MODE:** All TypeScript must be strictly typed
- **IMPORTS:** Use explicit imports for types (`import type { ... }`)
- **ERROR HANDLING:** Use `ApiError` class with type guards
- **ASYNC:** Always handle Promise rejections with try/catch

#### API Integration
- **CENTRALIZED:** Use `src/lib/utils/api.ts` for all backend calls
- **ERROR TYPES:** Use `ApiError<T>` with type guards (`isNotFound`, `isUnauthorized`, etc.)
- **AUTH:** JWT with automatic token refresh via `apiRequest()`
- **HELPERS:** Use `get()`, `post()`, `put()`, `del()`, `patch()` functions

#### Styling (Tailwind CSS v4)
- **CSS-FIRST:** Use `@import "tailwindcss"` in `app.css` - no JS config
- **UTILITY-FIRST:** Prefer Tailwind classes over custom CSS
- **RESPONSIVE:** Use mobile-first responsive design

#### i18n (Paraglide)
- **FUNCTION CALLS:** Messages are functions, not strings: `m.button_cancel()`
- **IMPORTS:** `import { m } from '$lib/paraglide/messages'`
- **REACTIVE:** Messages update reactively with locale changes

### Backend (Python + FastAPI)

#### Architecture Patterns
- **MODULAR ROUTERS:** Separate API features in `routers/` directory
- **MODELS:** Use Tortoise ORM models in `models.py`
- **SCHEMAS:** Explicit Pydantic request/response models
- **OWNERSHIP:** Enforce server-side ownership rules for data access

#### Code Conventions
- **FORMATTING:** Use `autopep8` for Python formatting
- **TYPE HINTS:** All functions must have proper type annotations
- **ERROR HANDLING:** Use FastAPI's HTTPException for API errors
- **ASYNC:** All route handlers must be async functions

#### Database Patterns
```python
# Correct Tortoise ORM pattern
class Pet(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    owner = fields.ForeignKeyField('models.User', related_name='pets')
    
    class Meta:
        table = "pets"

# Use pydantic_model_creator for responses
PetSchema = pydantic_model_creator(Pet, name='Pet')
```

## Testing Patterns

### Unit Tests (Vitest)
- **BROWSER CONTEXT:** Use `@vitest/browser` for DOM testing
- **SVELTE TESTING:** Use `vitest-browser-svelte` for component testing
- **PATTERNS:** `describe()`, `it()`, `expect.element()`

### E2E Tests (Playwright)
- **PAGE-BASED:** Simple page navigation and element testing
- **PATTERNS:** `test()`, `page.goto()`, `expect().toBeVisible()`

### Test File Organization
```
src/
├── lib/
│   └── components/
│       └── Button.test.ts      # Unit tests
└── routes/
    └── login.spec.ts           # E2E tests
```

## Project Structure

### Frontend Organization
```
apps/frontend/src/
├── lib/
│   ├── components/     # Reusable UI components
│   ├── utils/         # Helper functions (api.ts, auth.ts, etc.)
│   ├── stores/        # Svelte stores
│   ├── types/         # TypeScript definitions
│   └── paraglide/     # i18n messages
├── routes/            # SvelteKit pages + load functions
└── app.css           # Tailwind entry point
```

### Backend Organization
```
backend/
├── routers/           # API endpoint modules
├── models.py         # Database models
├── main.py           # FastAPI app entry
└── static/           # Static file serving
```

## Critical Gotchas

### Svelte 5 Migration
- **NO LEGACY:** Never import Svelte 4 lifecycle functions
- **RUNES ONLY:** Use `$state`, `$effect`, `$derived` for all reactivity
- **CUSTOM RULE:** ESLint rule `no-svelte-lifecycle` enforces this

### Paraglide i18n
- **FUNCTION CALLS:** Always call messages as functions: `m.button_cancel()`
- **NOT PROPERTIES:** Never access as properties: `m.button_cancel` (❌)

### API Integration
- **CENTRALIZED:** Always use `apiRequest()` helpers, never direct fetch
- **ERROR TYPES:** Use `ApiError` class with type guards for error handling
- **AUTH FLOW:** JWT tokens refresh automatically via `apiRequest()`

### Backend Database
- **TORTOISE ORM:** Use explicit field definitions in models
- **PYDANTIC SCHEMAS:** Create explicit request/response models
- **OWNERSHIP:** Enforce data access rules server-side

## Development Workflow

1. **Setup:** Run `pnpm install` and `cd backend && uv sync`
2. **Development:** Use `pnpm dev:all` to start both frontend and backend
3. **Code Quality:** Run `pnpm lint` before committing
4. **Testing:** Run `pnpm test` to ensure all tests pass
5. **Build:** Run `pnpm build` to verify production build

## API Endpoints Reference

Key endpoints for development:
- `POST /api/register` - User registration
- `POST /api/pets/` - Create pet
- `GET /api/pets/` - List user's pets
- `GET /api/pets/{id}` - Get pet details
- `PUT /api/pets/{id}` - Update pet
- `DELETE /api/pets/{id}` - Delete pet
- `GET /api/qrcode/{id}` - Generate QR code
- `GET /api/banners/{id}` - Generate lost pet banner

## Security Considerations

- **AUTH:** JWT tokens with automatic refresh
- **OWNERSHIP:** Server-side enforcement of data access rules
- **VALIDATION:** Use Pydantic schemas for request validation
- **CORS:** Proper CORS configuration for API access

## Performance Guidelines

- **BUNDLING:** Use SvelteKit's automatic code splitting
- **IMAGES:** Optimize images for web delivery
- **CACHING:** Implement appropriate caching strategies
- **DATABASE:** Use efficient queries with Tortoise ORM

## When in Doubt

1. **Check existing code** for patterns in the same domain
2. **Ask for clarification** on unclear requirements
3. **Follow established conventions** rather than introducing new patterns
4. **Test thoroughly** before submitting changes
5. **Run linting** to ensure code quality compliance