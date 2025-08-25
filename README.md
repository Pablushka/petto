# Doko

Doko is a Progressive Web Application designed to help reunite lost pets with their owners.

## Technologies

- **Backend:** Python 3, FastAPI, SQLite (scalable to MySQL)
- **Frontend:** SvelteKit 5, Prisma ORM, Tailwind CSS

## Backend Setup & Start Guide

### Prerequisites

- Python 3.8+
- (Recommended) Virtual environment tool: `venv` or `virtualenv`

### Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install fastapi tortoise-orm uvicorn
   ```
   (Add any other dependencies as needed)

### Running the Backend

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

- The API will be available at `http://127.0.0.1:8000`
- Health check endpoint: `GET /_health`

## Project Structure

- `backend/main.py`: FastAPI application entry point
- `backend/routers/`: API route modules (users, pets, qrcode, banners, pet_location)
- `backend/models.py`: Database models
- `backend/database.py`: Database configuration

## Additional Notes

- The backend uses SQLite by default. For production, consider switching to MySQL or PostgreSQL.
- API documentation is available at `/docs` when the server is running.

## Contributing

Pull requests and suggestions are welcome!

## License

Specify your license here.
