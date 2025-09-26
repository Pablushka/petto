# Petto Backend API Routes

## Pets

- `POST /pets/` — Create a pet
- `GET /pets/` — List pets
- `GET /pets/{pet_id}` — Get pet by ID
- `PUT /pets/{pet_id}` — Update pet
- `DELETE /pets/{pet_id}` — Delete pet

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

- `GET /` — Index page
- `GET /{page_name}` — Static page
