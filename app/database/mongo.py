from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.models.auth import Auth
from app.models.user import User
from app.models.company import Company

class MongoDB:
    client: AsyncMongoClient | None = None

    @classmethod
    async def connect_db(cls, uri: str):
        """
        Initialize and connect to MongoDB database
        """
        try:
            cls.client = AsyncMongoClient(uri)
            db = cls.client.get_default_database()
            await init_beanie(database=db, document_models=[Auth, User, Company])
            print(f"Database {db.name} connected")
            return db
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    @classmethod
    async def disconnect_db(cls):
        """
        Disconnect from MongoDB database
        """
        if cls.client:
            await cls.client.close()
            cls.client = None
            print("MongoDB disconnected")
        else:
            print("No MongoDB client connected")