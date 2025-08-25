from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(init_db())
