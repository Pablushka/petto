
import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from routers import static, users, pets, qrcode, banners, pet_location, upload, flyers
from config import settings
from middleware.security import SecurityHeadersMiddleware
from middleware.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from logging_config import app_logger


app = FastAPI(
    title="Petto API",
    description="API for Petto - Lost Pet Reunification App",
    version="1.0.0"
)

# Add rate limiting state to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

if settings.cors_origins:
    allowed_origins = [origin.strip()
                       for origin in settings.cors_origins.split(",") if origin.strip()]
else:
    allowed_origins = DEFAULT_ORIGINS

# Production-specific origins
if settings.environment == "production":
    allowed_origins = [
        "https://petto.app",
        "https://www.petto.app"
    ]

# Security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Restrictive CORS configuration for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Accept",
        "Origin"
    ]
)

app.include_router(static.router)
app.include_router(users.router)
app.include_router(pets.router)
app.include_router(qrcode.router)
app.include_router(banners.router)
app.include_router(pet_location.router)
app.include_router(upload.router)
app.include_router(flyers.router)


@app.get("/_health")
def read_root():
    return {"status": "ok"}


register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
