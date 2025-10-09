import redis.asyncio as redis
from app.conf.settings import settings

class RedisManager:
    url: str = settings.redis_url
    _client: redis.Redis | None = None

    @classmethod
    async def connect(cls):
        """Create a Redis connection"""
        if not cls._client:
            cls._client = await redis.from_url(
                cls.url,
                encoding="utf-8",
                decode_responses=True
            )  
              
    @classmethod
    async def close(cls):
        """Close redis connection"""        
        if cls._client:
            await cls._client.close()
            cls._client = None
            
    @classmethod
    async def get_client(cls) -> redis.Redis:
        """Return the current Redis client, connecting if needed."""
        if not cls._client:
            await cls.connect()
        assert cls._client is not None 
        return cls._client