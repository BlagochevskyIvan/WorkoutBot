from redis.asyncio import Redis
from config.cp_config import REDIS_URL

redis = Redis.from_url(url=REDIS_URL, decode_responses=True)