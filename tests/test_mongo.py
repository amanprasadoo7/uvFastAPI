import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def main():
    client = AsyncIOMotorClient(str(settings.mongo_url))
    db = client.test123
    collection = db.connection_tests

    insert_result = await collection.insert_one({
        "event": "db_write_test",
        "ok": True,
    })

    doc = await collection.find_one(
        {"_id": insert_result.inserted_id}
    )

    print("Inserted + fetched:", doc)

    client.close()

if __name__ == "__main__":
    asyncio.run(main())
