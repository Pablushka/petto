## Pet Schemas (Explicit)

This document describes the explicit Pydantic schemas used for Pet resources.

### Overview

| Schema | Purpose |
|--------|---------|
| `PetBase` | Core reusable fields (`name`, `pet_type`, `picture`, `notes`, `status`) |
| `PetCreate` | Create payload (currently still includes `owner_id` but ignored) |
| `PetUpdate` | Partial update payload (all optional) |
| `PetOut` | Response model (adds `id`, `owner_id`) |

### Enums

```
PetType   = Cat | Dog | Lizard | Hamster | Bird | Other
PetStatus = at_home | lost | found
```

### Ownership Enforcement

The backend overrides any client-provided `owner_id` with the authenticated user's id. This prevents privilege escalation attempts (e.g., assigning a pet to another user). A future breaking change will remove `owner_id` from `PetCreate` entirely once all clients are updated.

### Rationale for Explicit Schemas

1. Security boundary clarity
2. Stable public contract independent from ORM model evolution
3. Easier documentation and versioning
4. Flexible partial updates

### Future Enhancements

- Remove `owner_id` from `PetCreate`
- Introduce `PATCH /pets/{id}` endpoint (currently `PUT` handles updates)
- Add serializer helper function to reduce repetition
- Add validation (e.g., max lengths, allowed transitions for `status`)

### Example Payloads

Create:
```json
{
  "name": "Rex",
  "pet_type": "Dog",
  "picture": "https://example.com/rex.jpg",
  "notes": "Brown dog, friendly",
  "status": "lost"
}
```

Update (partial):
```json
{
  "status": "found"
}
```

Response (`PetOut`):
```json
{
  "id": 12,
  "owner_id": 3,
  "name": "Rex",
  "pet_type": "Dog",
  "picture": "https://example.com/rex.jpg",
  "notes": "Brown dog, friendly",
  "status": "lost"
}
```

---

For auth flow details see `Auth-Client-Side.md`.