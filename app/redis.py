import asyncio
import aioredis
from typing import Optional
from fastapi.applications import FastAPI

from typing import Optional

from aioredis import Redis, create_redis_pool


class RedisCache:
    
    def __init__(self, redis_host: str, redis_port: int, redis_db: int = 0, encoding: Optional[str] = 'utf-8'):
        self.redis_cache: Optional[Redis] = None
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.encoding = encoding
        
    async def init_cache(self):
        self.redis_cache = await create_redis_pool("redis://" + self.redis_host + ":" + str(self.redis_port) + "/" + str(self.redis_db), encoding=self.encoding)

    async def close(self):
        self.redis_cache.close()
        await self.redis_cache.wait_closed()

redis_cache = RedisCache("136.244.119.149", 6379)
