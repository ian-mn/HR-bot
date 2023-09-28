import abc

from redis.asyncio import Redis


class AbstractAuthStorage(abc.ABC):
    @abc.abstractmethod
    async def close(self):
        pass

    @abc.abstractmethod
    async def set(self, key, value):
        pass

    @abc.abstractmethod
    async def get(self, key):
        pass

    @abc.abstractmethod
    async def expire(self, key, seconds):
        pass


class RedisStorage(AbstractAuthStorage):
    def __init__(self, host: str, port: int):
        self.storage = Redis(host=host, port=port, decode_responses=True, encoding="utf-8")

    async def set(self, key, value):
        await self.storage.set(key, value)

    async def get(self, key):
        return await self.storage.get(key)

    async def expire(self, key, seconds):
        await self.storage.expire(key, seconds)

    async def close(self):
        await self.storage.close()


auth_storage: RedisStorage | None = None


async def get_auth_storage() -> Redis:
    return auth_storage.storage
