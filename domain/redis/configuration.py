import redis
from config.database import DatabaseConfig

class RedisClient:
    redis_client = redis.StrictRedis.from_url(DatabaseConfig.REDIS_URL, decode_responses=True)
