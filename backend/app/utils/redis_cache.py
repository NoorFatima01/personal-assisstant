import pickle

class RedisCache:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def make_key(self, *args):
        """Create a cache key from the given arguments."""
        return ":".join(map(str, args))

    def set_pickle(self, key:str, value:object, ttl:int=None):
        """Set a value in the Redis cache."""
        pickled = pickle.dumps(value)
        if ttl:
            self.redis_client.set(key, pickled, ex=ttl)
        else:
            self.redis_client.set(key, pickled)

    def set(self, key, value, ttl=None):
        if ttl:
            self.redis_client.set(key, value, ex=ttl)
        else:
            self.redis_client.set(key, value)

    def get(self, key):
        """Get a value from the Redis cache."""
        serialized_value = self.redis_client.get(key)
        if serialized_value is not None:
            return pickle.loads(serialized_value)
        return None

    def delete(self, key):
        """Delete a value from the Redis cache."""
        self.redis_client.delete(key)