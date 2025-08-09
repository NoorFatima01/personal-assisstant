import redis

redis_client = redis.Redis(
    host="localhost",  # or "127.0.0.1"
    port=6379,
    db=0,
    decode_responses=True  # returns strings instead of bytes
)
