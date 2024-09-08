from redis.asyncio.client import Redis
from llama_index.storage.chat_store.redis import RedisChatStore

def init_client () -> Redis | None:
    client = Redis(
            host = "localhost",
            port = 8083,
            decode_responses=True
            )

    try :
        if isinstance(client,Redis): 
            print("Redis Chat Client and KV Store connected successfully")
            return client
        else: print("Redis Chat Client is not ready. Check the Docker instance")

    except Exception as e:
        print(f"Error connecting to Redis: {e}")

    return None

if __name__ == "__main__" : 
    client = init_client()
    print("client created")
    index_store = RedisChatStore(
            redis_client= client,
            )

