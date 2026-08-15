import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

try:
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
except Exception as e:
    print(f"Warning: Failed to initialize Redis client: {e}")
    redis_client = None

def get_cached_data(key: str):
    if not redis_client:
        return None
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"Redis cache GET warning for key '{key}': {e}")
    return None

def set_cached_data(key: str, value: any, expire_seconds: int = 300):
    if not redis_client:
        return
    try:
        redis_client.set(key, json.dumps(value), ex=expire_seconds)
    except Exception as e:
        print(f"Redis cache SET warning for key '{key}': {e}")

def invalidate_cache(key: str):
    if not redis_client:
        return
    try:
        if "*" in key:
            keys = redis_client.keys(key)
            if keys:
                redis_client.delete(*keys)
        else:
            redis_client.delete(key)
    except Exception as e:
        print(f"Redis cache DELETE warning for key '{key}': {e}")
