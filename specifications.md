# Introduction

Doko is a Progressive Web Application to contact lost pets with their owners.

# Technologies Involved

Doko uses the following technologies:

## Backend

- Python 3 as the main language
- FastAPI as a lightweight REST development framework
- SQLite as the default database, with scalability options for MySQL

## Frontend

- SvelteKit 5
- Prisma ORM
- Tailwind CSS

# App Specifications

## Actors

- **Admin**: A user with full rights to manage all aspects of the system. There can be more than one admin user.
- **User**: A pet owner who uses the app to recover their pet in case of loss.
- **Billing Company**: A third-party service to bill users for using the app.

## Features & Functions

- **User Registration**: Form to input and store user data:

  - First Name
  - Last Name
  - Email
  - Phone
  - Full Address
  - Pets (collection of owned pets)
  - Recovery Bounty

- **Pet Registration**: Form (linked to User Registration) to input and store pet data:

  - Owner (User)
  - Name
  - Picture
  - Notes (any relevant information about the pet)

- **QR Code Functionality**:

  - QR Code generation: For each pet, the app generates a QR code linking to the owner's user profile.
  - User and pet data editing
  - QR Scan location: When the QR code is scanned, the owner is notified by email, and the scan location is saved and included in the notification.
  - The QR code link points to the user profile.

- **Lost Pet Banners**: The app generates templates for printing and sharing on social networks, with flyers about how to recover the lost pet.

---

## Suggestions for Improvement

- **Authentication & Security**: Consider adding user authentication (e.g., email/password, OAuth) and secure data handling.
- **Notifications**: Support additional notification methods (SMS, push notifications) for faster alerts.
- **Scalability**: Prepare for scaling the backend (e.g., support for PostgreSQL, cloud deployment).
- **Admin Dashboard**: Add an admin dashboard for managing users, pets, and system settings.
- **Audit Logs**: Track important actions (e.g., pet registration, QR scans) for security and troubleshooting.
- **API Documentation**: Provide OpenAPI documentation for backend endpoints.
- **Accessibility**: Ensure the frontend is accessible (WCAG compliance).
- **Internationalization**: Support multiple languages for broader reach.
