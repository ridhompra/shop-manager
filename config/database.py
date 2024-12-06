import os

class DatabaseConfig:
    POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/dbname")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class RedisKey:
    SHOPEE_ACCESS_TOKEN_KEY = "SHOPEE_ACCESS_TOKEN_KEY"
