import asyncio
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = str(settings.postgres_url)

async def test_db():
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        # Create table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS playing_with_neon (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                value REAL
            )
        """))

        # Insert data
        await conn.execute(text("""
            INSERT INTO playing_with_neon(name, value)
            SELECT LEFT(md5(i::TEXT), 10), random()
            FROM generate_series(1, 10) s(i)
        """))

        # Query data
        result = await conn.execute(
            text("SELECT * FROM playing_with_neon")
        )

        rows = result.fetchall()
        for row in rows:
            print(row)

    await engine.dispose()

asyncio.run(test_db())
