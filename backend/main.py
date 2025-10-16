
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from routers import static, users, pets, qrcode, banners, pet_location, upload, flyers


app = FastAPI()

DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

origins_env = os.getenv("CORS_ALLOWED_ORIGINS")
if origins_env:
    allowed_origins = [origin.strip()
                       for origin in origins_env.split(",") if origin.strip()]
else:
    allowed_origins = DEFAULT_ORIGINS

# CORS configuration for frontend dev server or production
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
