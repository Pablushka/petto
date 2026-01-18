# Petto

Petto is a Progressive Web Application designed to help reunite lost pets with their owners.

## Features

### Authentication & User Management
- **User Registration** - Create new accounts with email validation
- **Login/Logout** - Secure JWT-based authentication with access and refresh tokens
- **Password Recovery** - Request password reset tokens via email
- **Protected Routes** - Automatic token refresh and redirect for unauthorized access
- **Rate Limiting** - Protection against brute force attacks on auth endpoints

### Pet Management
- **Pet Collection** - Create, read, update, and delete pets
- **Multi-Image Upload** - Upload up to 5 images per pet with cover image selection
- **Image Reordering** - Arrange images before submission
- **Pet Status Tracking** - Track pet status: `at_home`, `lost`, or `found`
- **Pet Types** - Support for: Cat, Dog, Bird, Lizard, Hamster, and Other

### Lost Pet Features
- **QR Code Generation** - Generate unique QR codes for pet tags (square or circular)
- **Lost Pet Flyers** - Create print-ready A4 flyers with pet info and QR code
- **Location Tracking** - Record QR code scans with location data when pets are found
- **Scan History** - View all scan events for a specific pet

### Internationalization
- **Multi-language Support** - English, Spanish, and Japanese via Paraglide i18n
- **Reactive Locale Switching** - Messages update automatically on language change

## Technologies

- **Backend:** Python 3.13+, FastAPI, SQLite (upgradable to MySQL/PostgreSQL), Tortoise ORM, Uvicorn
- **Frontend:** SvelteKit 5, TypeScript, Tailwind CSS v4, Paraglide i18n, Prisma ORM
- **Testing:** Vitest (unit), Playwright (E2E)
- **Package Management:** pnpm (frontend), uv (backend)
- **Security:** JWT tokens, HTTP-only cookies, CORS, rate limiting, security headers

## Monorepo Structure

Petto uses pnpm workspaces for monorepo management:

```
petto/
├── backend/              # FastAPI backend
│   ├── routers/         # API endpoints (users, pets, qrcode, etc.)
│   ├── models.py        # Database models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── middleware/      # Security, rate limiting
│   └── utils/           # Auth helpers
├── apps/
│   └── frontend/        # SvelteKit frontend
│       ├── src/
│       │   ├── routes/  # Pages and layouts
│       │   ├── lib/     # Components, utilities, stores
│       │   └── paraglide/ # i18n messages
│       └── static/      # Static assets
└── packages/
    └── shared/          # Shared libraries (optional)
```

## Quick Start

### Prerequisites

- **Python:** 3.13+ (managed via uv)
- **Node.js:** 18+ (for pnpm and SvelteKit)
- **pnpm:** 10+ (package manager)
- **uv:** Python package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd petto
   ```

2. **Install frontend dependencies:**
   ```bash
   pnpm install
   ```

3. **Install backend dependencies:**
   ```bash
   cd backend
   uv sync
   cd ..
   ```

### Running the Application

#### Development Mode (Recommended)

Run both frontend and backend concurrently:

```bash
pnpm dev:all
```

This starts:
- **Frontend:** http://localhost:5173
- **Backend:** http://127.0.0.1:8000

#### Individual Services

**Frontend only:**
```bash
pnpm dev:frontend
# or
cd apps/frontend && pnpm dev
```

**Backend only:**
```bash
pnpm dev:backend
# or
cd backend && uv run uvicorn main:app --reload
```

### Production Build

**Build frontend:**
```bash
pnpm build
```

**Preview production build:**
```bash
pnpm preview
```

### Testing

**Run all tests:**
```bash
pnpm test
```

**Frontend tests:**
```bash
cd apps/frontend
pnpm test:unit      # Vitest unit tests
pnpm test:e2e       # Playwright E2E tests
```

**Linting:**
```bash
pnpm lint           # Lint all packages
```

## API Documentation

### Base URL

- Development: `http://127.0.0.1:8000`
- Production: Configure via environment variables

### Interactive API Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Health Check

```bash
# Check if backend is running
curl http://127.0.0.1:8000/_health
# Response: {"status": "ok"}
```

## Authentication & Authorization

Petto implements JWT-based authentication with access tokens (short-lived) and refresh tokens (long-lived).

### Authentication Flow

```mermaid
sequenceDiagram
   autonumber
   actor U as User
   participant FE as Frontend
   participant API as apiRequest()
   participant LS as LocalStorage
   participant BE as Backend

   Note over U,FE: User navigates to protected page
   U->>FE: Access /pets
   FE->>API: GET /api/users/me (requireAuth: true)
   
   alt No tokens in localStorage
      API-->>FE: 401 Unauthorized
      FE-->>U: Redirect to /login?returnUrl=/pets
   else Valid access_token
      API->>BE: GET /api/users/me (Bearer token)
      BE-->>API: 200 OK {user data}
      API-->>FE: Return user
      FE-->>U: Render protected page
   else Expired access_token
      API->>BE: GET /api/users/me
      BE-->>API: 401 Unauthorized
      API->>BE: POST /api/token/refresh {refresh_token}
      alt Valid refresh_token
         BE-->>API: {access_token, refresh_token}
         API->>LS: Update tokens
         API->>BE: Retry GET /api/users/me
         BE-->>API: 200 OK {user data}
         API-->>FE: Return user
         FE-->>U: Render protected page
      else Invalid refresh_token
         BE-->>API: 401 Unauthorized
         API->>LS: Clear tokens
         FE-->>U: Redirect to /login
      end
   end
```

### API Endpoints

#### User Registration

```bash
# Register new user
curl -X POST http://127.0.0.1:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "full_address": "123 Main St, City",
    "recovery_bounty": 50.0,
    "password": "SecurePassword123!"
  }'

# Response: 200 OK
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "full_address": "123 Main St, City",
  "recovery_bounty": 50.0
}
```

#### User Login

```bash
# Login with email and password
curl -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'

# Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Token Refresh

```bash
# Refresh expired access token
curl -X POST http://127.0.0.1:8000/api/token/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'

# Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Get Current User

```bash
# Get authenticated user details
curl -X GET http://127.0.0.1:8000/api/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Response: 200 OK
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "1234567890"
}
```

#### Password Recovery

```bash
# Request password recovery token
curl -X POST http://127.0.0.1:8000/api/password-recovery \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'

# Response: 200 OK
{
  "message": "Recovery email sent (stub)",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

# Reset password with token
curl -X POST http://127.0.0.1:8000/api/password-reset \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "new_password": "NewSecurePassword123!"
  }'

# Response: 200 OK
{
  "message": "Password reset successful"
}
```

### Pet Management Endpoints

#### Create Pet

```bash
# Create new pet (requires authentication)
curl -X POST http://127.0.0.1:8000/api/pets/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Max",
    "pet_type": "Dog",
    "picture": "https://example.com/max.jpg",
    "pictures": [
      "https://example.com/max.jpg",
      "https://example.com/max2.jpg"
    ],
    "notes": "Friendly golden retriever, loves treats",
    "status": "at_home"
  }'

# Response: 200 OK
{
  "id": 1,
  "owner_id": 1,
  "name": "Max",
  "pet_type": "Dog",
  "picture": "https://example.com/max.jpg",
  "pictures": [
    "https://example.com/max.jpg",
    "https://example.com/max2.jpg"
  ],
  "notes": "Friendly golden retriever, loves treats",
  "status": "at_home"
}
```

#### List User's Pets

```bash
# Get all pets for authenticated user
curl -X GET http://127.0.0.1:8000/api/pets/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response: 200 OK
[
  {
    "id": 1,
    "owner_id": 1,
    "name": "Max",
    "pet_type": "Dog",
    "picture": "https://example.com/max.jpg",
    "pictures": ["https://example.com/max.jpg", "..."],
    "notes": "Friendly golden retriever",
    "status": "at_home"
  }
]
```

#### Get Pet by ID

```bash
# Get specific pet details
curl -X GET http://127.0.0.1:8000/api/pets/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response: 200 OK
{
  "id": 1,
  "owner_id": 1,
  "name": "Max",
  "pet_type": "Dog",
  "status": "at_home",
  ...
}
```

#### Update Pet

```bash
# Update pet information
curl -X PUT http://127.0.0.1:8000/api/pets/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Max Updated",
    "status": "lost",
    "notes": "Lost near Central Park on Jan 15"
  }'

# Response: 200 OK
{
  "id": 1,
  "name": "Max Updated",
  "status": "lost",
  ...
}
```

#### Delete Pet

```bash
# Delete a pet
curl -X DELETE http://127.0.0.1:8000/api/pets/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response: 200 OK
{
  "message": "Pet deleted successfully"
}
```

### QR Code & Location Endpoints

#### Generate QR Code

```bash
# Generate QR code for pet
curl -X GET http://127.0.0.1:8000/api/qrcode/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Returns PNG image
```

#### Record QR Scan

```bash
# Record when someone scans the pet's QR code
curl -X POST http://127.0.0.1:8000/api/pet-location/scan \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": 1,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "notes": "Found near subway station"
  }'

# Response: 200 OK
{
  "id": 1,
  "pet_id": 1,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": "2026-01-18T10:30:00",
  "notes": "Found near subway station"
}
```

#### Get Pet QR Link

```bash
# Get shareable QR link for pet
curl -X GET http://127.0.0.1:8000/api/pet-location/pet/1/qr-link \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response: 200 OK
{
  "qr_link": "https://petto.app/scan/abc123xyz"
}
```

#### Get Scan History

```bash
# Get all scan events for a pet
curl -X GET http://127.0.0.1:8000/api/pet-location/pet/1/scans \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Response: 200 OK
[
  {
    "id": 1,
    "pet_id": 1,
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timestamp": "2026-01-18T10:30:00",
    "notes": "Found near subway station"
  }
]
```

### Flyer Generation

```bash
# Generate lost pet flyer (HTML/PDF ready)
curl -X GET http://127.0.0.1:8000/api/flyers/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Returns HTML document ready for printing
```

## Frontend Integration

### API Helper Functions

The frontend uses centralized API utilities in `src/lib/utils/api.ts`:

```typescript
import { get, post, put, del } from '$lib/utils/api';

// Login
const { access_token, refresh_token } = await post('/api/login', {
  body: { email: 'user@example.com', password: 'password' }
});

// Get current user (auto-adds Authorization header)
const user = await get('/api/users/me', { requireAuth: true });

// Create pet
const newPet = await post('/api/pets/', {
  body: { name: 'Max', pet_type: 'Dog', status: 'at_home' },
  requireAuth: true
});

// Update pet
const updated = await put('/api/pets/1', {
  body: { status: 'lost' },
  requireAuth: true
});

// Delete pet
await del('/api/pets/1', { requireAuth: true });
```

### Error Handling

```typescript
import { isNotFound, isUnauthorized, ApiError } from '$lib/utils/api';

try {
  const pet = await get('/api/pets/999', { requireAuth: true });
} catch (error) {
  if (isNotFound(error)) {
    console.error('Pet not found');
  } else if (isUnauthorized(error)) {
    console.error('Not authenticated');
    goto('/login');
  } else if (error instanceof ApiError) {
    console.error(`API Error ${error.status}: ${error.message}`);
  }
}
```

### Automatic Token Refresh

The `apiRequest()` function automatically:
1. Adds `Authorization: Bearer <token>` header for authenticated requests
2. Detects 401 errors and attempts token refresh
3. Retries the original request with new tokens
4. Redirects to login if refresh fails

### Protected Routes

Use the `ProtectedRoute` component or `protect-route` utility:

```svelte
<script>
  import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
</script>

<ProtectedRoute>
  <!-- Only renders if user is authenticated -->
  <h1>My Pets</h1>
  <!-- Pet list here -->
</ProtectedRoute>
```

## Data Models & Schemas

### Pet Data Model

The Pet API uses **explicit Pydantic schemas** for type safety and validation:

| Schema | Purpose | Key Fields |
|--------|---------|------------|
| `PetBase` | Shared core fields | `name`, `pet_type`, `picture`, `notes`, `status` |
| `PetCreate` | Create payload | Inherits `PetBase` + optional `owner_id` (ignored, uses auth user) |
| `PetUpdate` | Update payload (partial) | All fields optional |
| `PetOut` | Response model | `id`, `owner_id`, + `PetBase` fields + `pictures[]` array |

#### Pet Types & Status

```typescript
// Pet Types (enum)
type PetType = 'Cat' | 'Dog' | 'Bird' | 'Lizard' | 'Hamster' | 'Other';

// Pet Status (enum)
type PetStatus = 'at_home' | 'lost' | 'found';
```

#### Multi-Image Support

The backend stores up to 5 images per pet:
- `picture` (required) - Cover image (also `pictures[0]`)
- `picture2` through `picture5` (optional) - Additional images

The API normalizes these into a single `pictures[]` array:

```json
{
  "id": 1,
  "name": "Max",
  "picture": "https://example.com/max.jpg",
  "pictures": [
    "https://example.com/max.jpg",    // Cover (picture)
    "https://example.com/max2.jpg",   // picture2
    "https://example.com/max3.jpg"    // picture3
  ]
}
```

**Frontend helpers:**
- `getPetCover(pet)` - Returns cover image URL with fallback

#### Security: Owner Enforcement

**Critical:** The backend **always overrides** `owner_id` with the authenticated user's ID. Users can only access/modify their own pets.

### User Data Model

```typescript
interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  full_address: string;
  recovery_bounty: number;  // Reward amount for finding lost pet
  password: string;         // Hashed (never returned in API)
}
```

### Location/Scan Data Model

```typescript
interface PetScan {
  id: number;
  pet_id: number;
  latitude: number;
  longitude: number;
  timestamp: string;        // ISO 8601 datetime
  notes?: string;
}
```

## Backend Architecture

### Project Structure

```
backend/
├── main.py                 # FastAPI app, CORS, middleware
├── models.py              # Tortoise ORM models
├── database.py            # DB configuration
├── config.py              # Environment settings
├── routers/               # API endpoints
│   ├── users.py          # Auth, registration, password recovery
│   ├── pets.py           # Pet CRUD operations
│   ├── qrcode.py         # QR code generation
│   ├── banners.py        # Banner image generation
│   ├── flyers.py         # Lost pet flyer generation
│   ├── pet_location.py   # Scan tracking, location
│   ├── upload.py         # File uploads
│   └── static.py         # Static file serving
├── schemas/               # Pydantic request/response models
│   ├── users.py
│   ├── pets.py
│   └── location.py
├── middleware/            # Security & rate limiting
│   ├── security.py       # Security headers
│   └── rate_limit.py     # Rate limiting config
├── utils/
│   └── auth.py           # JWT utilities, password hashing
└── static/
    ├── templates/        # HTML templates
    └── uploads/          # User-uploaded files
```

### Middleware & Security

**Security Headers:**
- Content Security Policy (CSP)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Strict-Transport-Security (HSTS)

**CORS Configuration:**
- Development: `http://localhost:5173`, `http://127.0.0.1:5173`
- Production: `https://petto.app`, `https://www.petto.app`
- Credentials: Enabled for cookie-based auth

**Rate Limiting:**
- Login: 5 requests per minute
- Registration: 3 requests per minute
- General API: 100 requests per minute
- Configurable via `middleware/rate_limit.py`

### Database

**Default:** SQLite (`db.sqlite3`)
- Fast development setup
- Zero configuration
- Single-file database

**Production Recommendations:**
- PostgreSQL (scalable, robust)
- MySQL (widely supported)

**Configure via `backend/config.py`:**
```python
DATABASE_URL = "sqlite://db.sqlite3"
# or
DATABASE_URL = "postgres://user:password@host:port/dbname"
```

### Environment Configuration

Create `backend/.env`:

```env
# Database
DATABASE_URL=sqlite://db.sqlite3

# JWT Secrets (CHANGE IN PRODUCTION!)
SECRET_KEY=your-secret-key-here-min-32-chars
REFRESH_SECRET_KEY=your-refresh-secret-key-here

# CORS
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
ENVIRONMENT=development

# Optional: Rate limiting
RATE_LIMIT_ENABLED=true
```

## Frontend Architecture

### Project Structure

```
apps/frontend/
├── src/
│   ├── routes/                  # SvelteKit pages
│   │   ├── +layout.svelte      # Root layout
│   │   ├── +layout.ts          # Load user session
│   │   ├── +page.svelte        # Homepage
│   │   ├── login/              # Login page
│   │   ├── pets/               # Pet management
│   │   ├── flyers/             # Flyer generator
│   │   └── forgot-password/    # Password recovery
│   ├── lib/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Button.svelte
│   │   │   ├── Modal.svelte
│   │   │   ├── Alert.svelte
│   │   │   ├── ProtectedRoute.svelte
│   │   │   └── ...
│   │   ├── utils/
│   │   │   ├── api.ts          # API helpers (get, post, put, del)
│   │   │   ├── auth.ts         # Token management
│   │   │   └── pet.ts          # Pet utility functions
│   │   ├── stores/
│   │   │   └── session.ts      # User session store
│   │   ├── types/              # TypeScript definitions
│   │   └── paraglide/          # i18n messages
│   ├── app.css                 # Tailwind CSS entry
│   └── app.html                # HTML template
├── static/
│   ├── flyers_templates/       # Flyer HTML/CSS templates
│   └── robots.txt
├── svelte.config.js            # SvelteKit config
├── vite.config.ts              # Vite config
├── tailwind.config.js          # Tailwind config (if any)
├── playwright.config.ts        # E2E test config
└── vitest-setup-client.ts      # Vitest config
```

### Key Frontend Concepts

#### Svelte 5 Runes (MANDATORY)

**DO NOT use Svelte 4 lifecycle functions!**

✅ **Correct (Svelte 5):**
```svelte
<script lang="ts">
  let count = $state(0);
  
  $effect(() => {
    console.log('Count changed:', count);
  });
  
  const doubled = $derived(count * 2);
</script>
```

❌ **Incorrect (Svelte 4 - BANNED):**
```svelte
<script lang="ts">
  import { onMount } from 'svelte';  // ❌ NO!
  
  onMount(() => {  // ❌ NO!
    // ...
  });
</script>
```

#### Tailwind CSS v4

Use CSS-first approach with `@import "tailwindcss"` in `app.css`:

```css
@import "tailwindcss";

/* Custom styles */
.btn {
  @apply px-4 py-2 rounded bg-blue-500 text-white;
}
```

#### Internationalization (Paraglide)

**Messages are functions, not strings!**

```typescript
// ❌ Wrong
import { m } from '$lib/paraglide/messages';
const text = m.button_cancel;  // Error!

// ✅ Correct
import { m } from '$lib/paraglide/messages';
const text = m.button_cancel();  // Function call
```

**Locale switching:**
```typescript
import { setLocale } from '$lib/paraglide/runtime';

setLocale('es');  // Switch to Spanish
setLocale('en');  // Switch to English
setLocale('jp');  // Switch to Japanese
```

### Frontend Development Workflow

```bash
# Start dev server
pnpm dev

# Type checking
pnpm check

# Watch mode for type checking
pnpm check:watch

# Linting
pnpm lint

# Format code
pnpm format

# Run unit tests
pnpm test:unit

# Run E2E tests
pnpm test:e2e

# Check for Svelte 4 lifecycle usage
pnpm lint:svelte-runes
```

## Testing

### Unit Tests (Vitest)

Located in `src/**/*.test.ts`:

```typescript
import { describe, it, expect } from 'vitest';
import { render } from 'vitest-browser-svelte';
import Button from './Button.svelte';

describe('Button', () => {
  it('renders with text', async () => {
    const { getByText } = render(Button, { 
      props: { text: 'Click me' } 
    });
    
    await expect.element(getByText('Click me')).toBeVisible();
  });
});
```

**Run tests:**
```bash
pnpm test:unit
# or specific file
pnpm test:unit src/lib/components/Button.test.ts
```

### E2E Tests (Playwright)

Located in `src/**/*.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';

test('login page loads', async ({ page }) => {
  await page.goto('/login');
  await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
});
```

**Run tests:**
```bash
pnpm test:e2e
# or specific file
pnpm test:e2e src/routes/login/page.spec.ts
```

## Common Development Tasks

### Adding a New API Endpoint

1. **Define schema** in `backend/schemas/`:
   ```python
   # schemas/my_feature.py
   from pydantic import BaseModel
   
   class MyFeatureCreate(BaseModel):
       name: str
       description: str
   ```

2. **Create router** in `backend/routers/`:
   ```python
   # routers/my_feature.py
   from fastapi import APIRouter, Depends
   from utils.auth import get_current_user
   
   router = APIRouter(prefix="/api", tags=["MyFeature"])
   
   @router.post("/my-feature/")
   async def create_feature(
       data: MyFeatureCreate,
       current_user = Depends(get_current_user)
   ):
       # Implementation
       return {"status": "created"}
   ```

3. **Register router** in `backend/main.py`:
   ```python
   from routers import my_feature
   
   app.include_router(my_feature.router)
   ```

### Creating a New Frontend Page

1. **Create route folder:**
   ```bash
   mkdir -p apps/frontend/src/routes/my-page
   ```

2. **Add page component:**
   ```svelte
   <!-- apps/frontend/src/routes/my-page/+page.svelte -->
   <script lang="ts">
     import { m } from '$lib/paraglide/messages';
   </script>

   <h1>{m.my_page_title()}</h1>
   ```

3. **Add i18n messages** (if needed):
   ```json
   // messages/en.json
   {
     "my_page_title": "My Page"
   }
   ```

### Adding Protected Content

```svelte
<script lang="ts">
  import ProtectedRoute from '$lib/components/ProtectedRoute.svelte';
</script>

<ProtectedRoute>
  <!-- Only visible to authenticated users -->
  <h1>Private Content</h1>
</ProtectedRoute>
```

## Troubleshooting

### Backend Issues

**Database locked error:**
```bash
# Stop all running backend instances
pkill -f uvicorn
# Restart backend
cd backend && uv run uvicorn main:app --reload
```

**Import errors:**
```bash
# Resync dependencies
cd backend && uv sync
```

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Module not found:**
```bash
# Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

**Type errors:**
```bash
# Regenerate Svelte types
pnpm check
```

**Tailwind styles not applying:**
```bash
# Clear Vite cache
rm -rf apps/frontend/.svelte-kit apps/frontend/node_modules/.vite
pnpm dev
```

## Deployment

### Backend Deployment

**Requirements:**
- Python 3.13+
- uv package manager
- PostgreSQL (recommended for production)

**Steps:**
1. Set environment variables (`.env` or platform config)
2. Update `DATABASE_URL` to production database
3. Generate strong `SECRET_KEY` and `REFRESH_SECRET_KEY`
4. Set `ENVIRONMENT=production`
5. Configure `CORS_ORIGINS` to production domain
6. Run: `uv run uvicorn main:app --host 0.0.0.0 --port 8000`

**Example (Docker):**
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY backend/ .
RUN pip install uv && uv sync
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Frontend Deployment

**Build:**
```bash
cd apps/frontend
pnpm build
```

**Outputs:** `apps/frontend/build/` (adapter-dependent)

**Deploy to:**
- Vercel (recommended for SvelteKit)
- Netlify
- Cloudflare Pages
- Node.js server (adapter-node)

**Environment variables:**
```env
VITE_BACKEND_URL=https://api.petto.app
```

## Contributing

### Code Style

- **Backend:** Follow PEP 8, use `autopep8`
- **Frontend:** Use Prettier, ESLint
- **Commits:** Conventional commits format

### Before Submitting PR

```bash
# Run all checks
pnpm lint
pnpm test
pnpm build

# Backend checks
cd backend
uv run autopep8 .
```

### Guidelines

1. ✅ Use Svelte 5 runes only (NO Svelte 4 lifecycle)
2. ✅ Call Paraglide messages as functions
3. ✅ Use centralized API helpers (`api.ts`)
4. ✅ Enforce ownership rules server-side
5. ✅ Add tests for new features
6. ✅ Update README for significant changes

## License

[Specify your license here - e.g., MIT, Apache 2.0, etc.]

## Support & Resources

- **Documentation:** This README and `AGENTS.md`
- **API Docs:** http://127.0.0.1:8000/docs (when backend is running)
- **Issues:** [GitHub Issues]
- **Discussions:** [GitHub Discussions]

---

**Built with ❤️ for reuniting pets with their families**
