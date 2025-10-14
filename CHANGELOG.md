# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres (aspirationally) to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Explicit Pet Pydantic schemas: `PetBase`, `PetCreate`, `PetUpdate`, `PetOut` replacing auto-generated `PetIn` / `PetOut`.
- Serializer helpers: `serialize_pet`, `serialize_pet_list` for consistent, explicit response shaping.
- Documentation updates across root `README.md`, backend `README.md`, and `.github/docs/Pet-Schemas.md`.
- Authenticated image upload endpoint `POST /api/upload` (local disk, size/type validation, returns static URL).
- Multi-image pet support: up to 5 images per pet (`picture` + `picture2..5`) exposed as ordered `pictures[]` in `PetOut`.
- Frontend multi-image form with previews, reordering (drag-lite via up/down controls), removal, and sequential uploads.
- Shared frontend helper `getPetCover(pet)` + `DEFAULT_PET_IMAGE` constant to unify cover selection logic.

### Changed
- Ownership now enforced server-side: incoming `owner_id` is overridden with authenticated user id.
- Pets router refactored to remove manual inline `PetOut.model_validate` constructions.
- Update endpoint now performs queryset `.update()` to avoid partial instance state errors during multi-image updates.

### Deprecated
- Supplying `owner_id` in create/update payloads (will be ignored and later removed from `PetCreate`).
- Direct component-level cover resolution logic (migrate to `getPetCover`).

### Security
- Eliminated possibility of privilege escalation by forging `owner_id` in pet creation/update.

### Planned
- Remove `owner_id` from `PetCreate` once frontend updated.
- Introduce `PATCH /api/pets/{id}` using `PetUpdate`.
- Add unit tests for serialization and ownership enforcement.
- Add status transition rules (e.g., `found` after `lost`).
- Add edit form parity for multi-image reordering / replacement.
- Consider migration to separate images table or JSON column for scalability.

## [0.1.0] - 2025-09-01
### Added
- Initial project structure (FastAPI backend + SvelteKit 5 frontend).
- User authentication with access + refresh tokens.
- Pets CRUD, QR code generation, banners endpoint scaffold.
- Basic i18n integration (Paraglide) and error localization.

[Unreleased]: https://example.com/compare/v0.1.0...HEAD
[0.1.0]: https://example.com/releases/v0.1.0
