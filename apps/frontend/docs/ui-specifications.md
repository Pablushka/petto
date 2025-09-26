# Petto PWA UI Specifications

## Overview

Petto is a Progressive Web App (PWA) for reuniting lost pets with their owners. The frontend is built with SvelteKit 5, Tailwind CSS, and Paraglide for i18n. This document outlines the UI specifications, component structure, and required tool versions for development.

---

## Tooling & Versions

- **SvelteKit:** ^2.36.2 (compatible with Svelte 4)
- **Svelte:** ^4.x
- **Tailwind CSS:** ^3.x
- **@tailwindcss/forms:** ^0.5.x
- **@tailwindcss/typography:** ^0.5.x
- **Paraglide JS:** ^3.x (for i18n)
- **Vite:** ^5.x
- **Playwright:** ^1.55.x (E2E tests)
- **Vitest:** ^3.x (unit tests)

---

## Layout Structure

- **Header:**
  - App logo (SVG favicon)
  - App name (Petto)
  - Navigation menu (Home, Pets, Login, Auth Test, Demo)
  - Language switcher (EN, ES, JP)
  - Responsive hamburger menu for mobile
  - User info (if logged in)
- **Main:**
  - Content slot for routed pages
  - Container with padding and max width
- **Footer:**
  - Copyright
  - Simple, unobtrusive style

---

## Navigation

- Use SvelteKit `<a href="/route">` for navigation.
- Responsive menu: horizontal on desktop, collapsible on mobile.
- Highlight active route (optional for future enhancement).

---

## Styling

- Use Tailwind utility classes for all styling.
- Forms use `@tailwindcss/forms` for consistent input styles.
- Typography plugin for rich text areas.
- Colors: blue accents for branding, gray backgrounds, white cards.
- Rounded corners, subtle shadows for cards and modals.
- Status indicators: color-coded badges for pet status (lost, found, reunited)

---

## Core Components

### Layout Components

- **Layout** (`+layout.svelte`): Main app layout with header, navigation, and footer

### UI Components

- **Button** (`Button.svelte`):
  - Types: primary, secondary, danger, success, warning
  - Sizes: sm, md, lg
  - States: default, loading, disabled
  - Options: fullWidth
- **TextField** (`TextField.svelte`):
  - Input with label and error handling
  - Supports various input types and validation
- **Select** (`Select.svelte`):
  - Dropdown select with options
  - Support for placeholder and error states
- **Alert** (`Alert.svelte`):
  - Types: error, success, info, warning
  - Dismissible option
- **Modal** (`Modal.svelte`):
  - Customizable size
  - Header, content, and optional footer slots
  - Keyboard/click dismissal
- **Pagination** (`Pagination.svelte`):
  - Numbered page navigation
  - Previous/next buttons
  - Dynamic page number display
- **LoadingState** (`LoadingState.svelte`):
  - Loading spinner
  - Empty state message
- **PageHeader** (`PageHeader.svelte`):
  - Consistent page title formatting
  - Optional subtitle

### Pet-Related Components

- **PetCard** (`pets/PetCard.svelte`):
  - Card displaying pet preview with image
  - Status badge
  - Key information display
- **PetDetail** (`pets/PetDetail.svelte`):
  - Detailed pet information display
  - Contact modal
  - Sighting report functionality
- **PetForm** (`pets/PetForm.svelte`):
  - Form for reporting lost/found pets
  - Image upload
  - Status toggle
- **PetList** (`pets/PetList.svelte`):
  - Searchable, filterable pet listings
  - Pagination
  - Status filtering

---

## Pages

- **Home** (`/`): Landing page with app features and quick actions
- **Pets** (`/pets`): List of lost and found pets with search/filter
- **Pet Detail** (`/pets/[id]`): Detailed information about a specific pet
- **Report Pet** (`/pets/report`): Form to report lost or found pets
- **Login** (`/login`): User authentication
- **Forgot Password** (`/forgot-password`): Password recovery
- **Auth Test** (`/auth-test`): Authentication testing page
- **Demo** (`/demo`): Feature demonstration pages

---

## i18n

- Use Paraglide messages as functions: `m.button_submit()`
- Do not access messages as properties
- Locale switching updates UI reactively
- Messages include general UI strings, pet-related terms, and form labels

---

## Pet Status Workflow

- **Lost**: Pets reported as lost by owners
- **Found**: Pets reported as found by community members
- **Reunited**: Pets that have been returned to owners

---

## Accessibility

- Use semantic HTML elements
- Ensure color contrast for readability
- Keyboard navigation for menus and forms
- ARIA attributes for dynamic components
  - `aria-label` for buttons without visible text (e.g., close buttons)
  - `aria-expanded` for toggle buttons (e.g., mobile menu)
  - `aria-current` for pagination to indicate current page
  - `aria-modal` and `aria-labelledby` for modal dialogs
  - `aria-live` regions for dynamic content updates
- Focus management for modal dialogs and popups
- Error states with clear messaging
- Responsive design with appropriate touch targets

---

## File Structure

```
apps/frontend/
├── src/
│   ├── routes/
│   │   ├── +layout.svelte           # Main app layout
│   │   ├── +page.svelte             # Homepage
│   │   ├── login/+page.svelte       # Login page
│   │   ├── forgot-password/+page.svelte
│   │   ├── auth-test/+page.svelte
│   │   ├── demo/+page.svelte
│   │   ├── pets/
│   │   │   ├── +page.svelte         # Pet listings
│   │   │   ├── [id]/+page.svelte    # Pet detail
│   │   │   └── report/+page.svelte  # Report pet form
│   ├── lib/
│   │   ├── components/
│   │   │   ├── Alert.svelte
│   │   │   ├── Button.svelte
│   │   │   ├── LoadingState.svelte
│   │   │   ├── Modal.svelte
│   │   │   ├── PageHeader.svelte
│   │   │   ├── Pagination.svelte
│   │   │   ├── Select.svelte
│   │   │   ├── TextField.svelte
│   │   │   └── pets/
│   │   │       ├── PetCard.svelte
│   │   │       ├── PetDetail.svelte
│   │   │       ├── PetForm.svelte
│   │   │       └── PetList.svelte
│   │   ├── paraglide/
│   │   │   └── messages/
│   │   └── stores/
│   │       └── session.ts
│   └── app.css                      # Tailwind imports
└── static/
    └── placeholder-pet.jpg          # Default pet image
```

---

## Testing

- **Unit:** Vitest (`pnpm run test:unit`)
- **E2E:** Playwright (`pnpm run test:e2e`)
- **Lint/Format:** Prettier, ESLint, Tailwind plugin

---

## References

- [SvelteKit Docs](https://kit.svelte.dev/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Paraglide JS Docs](https://inlang.com/m/gerre34r)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/standards-guidelines/wcag/)

---

## Future Enhancements

- Theme switcher (dark/light mode)
- Map integration for lost/found locations
- QR code generation for lost pet posters
- Notification system for potential matches
- User profile management
- Advanced accessibility features (screen reader announcements, keyboard shortcuts)
- Image optimization and lazy loading
- Offline capabilities with service workers

---

## Testing

- **Unit:** Vitest (`pnpm run test:unit`)
- **E2E:** Playwright (`pnpm run test:e2e`)
- **Lint/Format:** Prettier, ESLint, Tailwind plugin

---

## References

- [SvelteKit Docs](https://kit.svelte.dev/docs)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Paraglide JS Docs](https://inlang.com/m/gerre34r)

---

## Notes

- Update this document as UI evolves.
- Follow conventions in `README.md` and `.github/copilot-instructions.md`.
