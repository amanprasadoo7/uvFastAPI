import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings

async def main():
    assert settings.sqlite_url, "SQLITE_URL not set"

    engine = create_async_engine(settings.sqlite_url, echo=True)

    async with engine.begin() as conn:
        await conn.execute(text("CREATE TABLE IF NOT EXISTS test (id INTEGER)"))
        await conn.execute(text("INSERT INTO test (id) VALUES (1)"))
        result = await conn.execute(text("SELECT * FROM test"))
        print(result.fetchall())

    await engine.dispose()
    print("✅ SQLite connected")

if __name__ == "__main__":
    asyncio.run(main())
