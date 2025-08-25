from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routers import static, users, pets, qrcode, banners, pet_location

app = FastAPI()

app.include_router(static.router)
app.include_router(users.router)
app.include_router(pets.router)
app.include_router(qrcode.router)
app.include_router(banners.router)
app.include_router(pet_location.router)


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
