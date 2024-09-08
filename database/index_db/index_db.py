from redis.asyncio.client import Redis
from llama_index.storage.kvstore.redis import RedisKVStore
from llama_index.storage.index_store.redis import RedisIndexStore

def init_client () -> RedisKVStore | None:
    client = Redis(
            host = "localhost",
            port = 8081,
            decode_responses=True
            )

    assert isinstance(client,Redis), "Redis client broken"

    redis_kv_store = RedisKVStore(
            async_redis_client = client
            )

    try:
        if redis_kv_store :
            print("Redis Index Client and KV Store connected successfully")
            return redis_kv_store
        else: print("Redis Index Client is not ready. Check the Docker instance")
    
    except Exception as e:
        print(f"Error connecting to Redis: {e}")

    return None

if __name__ == "__main__" : 
    kv_store = init_client()
    print("kv store created")
    index_store = RedisIndexStore(
            redis_kvstore= kv_store,
            namespace= "index store"
            )

