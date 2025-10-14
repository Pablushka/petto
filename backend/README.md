# Petto Backend API Routes

## Pets

- `POST /pets/` — Create a pet
- `GET /pets/` — List pets
- `GET /pets/{pet_id}` — Get pet by ID
- `PUT /pets/{pet_id}` — Update pet
- `DELETE /pets/{pet_id}` — Delete pet

### Data Models (Explicit Schemas)

The pets API now uses explicit Pydantic schemas instead of the previous auto-generated `PetIn` / `PetOut`.

| Schema | Used For | Notes |
|--------|----------|-------|
| `PetBase` | Internal shared fields | `name`, `pet_type`, `picture`, `notes`, `status` (default `at_home`) |
| `PetCreate` | Request body for create | Inherits `PetBase` + `owner_id` (deprecated; server overrides) |
| `PetUpdate` | Request body for update | All fields optional for partial updates (current route still uses PUT) |
| `PetOut` | Response model | `id`, `owner_id`, plus base fields |

Enums:
```
PetType   = Cat | Dog | Lizard | Hamster | Bird | Other
PetStatus = at_home | lost | found
```

Security: `owner_id` in incoming payloads is ignored/overridden with the authenticated user (`current_user.id`). Frontend will be updated to stop sending it.

Migration rationale:
- Avoid accidental exposure of future ORM-only fields.
- Enable partial update semantics (`PetUpdate`).
- Make ownership enforcement explicit.
- Create a stable contract for third-party clients.

Deprecated: clients should stop sending `owner_id` in create/update; server keeps backward compatibility temporarily.

## Users

- `POST /register` — Register user
- `POST /password-recovery` — Request password recovery
- `POST /password-reset` — Reset password
- `POST /users/` — Create user
- `POST /login` — Login
- `POST /login/OAuth2` — OAuth2 login
- `GET /users/me` — Get current user
- `GET /users/` — List users
- `GET /users/{user_id}` — Get user by ID
- `PUT /users/{user_id}` — Update user
- `DELETE /users/{user_id}` — Delete user

## Banners

- `GET /banners/{pet_id}` — Get banners for pet

## QR Code

- `GET /qrcode/{pet_id}` — Get QR code for pet
- `POST /qrcode/scan/{scan_id}` — Scan QR code

## Pet Location

- `POST /scan` — Record scan
- `GET /pet/{pet_id}/qr-link` — Get QR link for pet
- `GET /pet/{pet_id}/scans` — Get scans for pet

## Static
## Upload

- `POST /upload` — Authenticated image upload (jpeg/png/webp/gif, max 5MB) returns `{ "url": "/static/uploads/<filename>" }`.


- `GET /` — Index page
- `GET /{page_name}` — Static page
