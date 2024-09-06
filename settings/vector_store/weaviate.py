import weaviate
from llama_index.vector_stores.weaviate import WeaviateVectorStore 
from llama_index.core import StorageContext
import dotenv
import os

# loading environmental variables 
dotenv.load_dotenv()
HUGGING_FACE_KEY = os.getenv("HUGGING_FACE_KEY")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")


# create client
def init_client(embed_model: str) -> weaviate.WeaviateClient | None: 
    if not HUGGING_FACE_KEY:
        raise ValueError("HUGGING_FACE_KEY is not set in the environment variables.")

    if embed_model.split('/') != "sentence-transformers":
        embed_model = "sentence-transformers/" + embed_model
    
    print(f"model name is {embed_model}")

    # client init
    client = weaviate.connect_to_custom(
        http_host="localhost",
        http_port=8080,
        http_secure=False,
        grpc_host="localhost",
        grpc_port=50051,
        grpc_secure=False,
        headers={"hugging-face-key": HUGGING_FACE_KEY}
    )

    try:
        if client.is_ready():
            print("Weaviate is ready and the client is connected successfully.")
            return client
        else: print("Weaviate is not ready. Check the Docker instance.")

    except Exception as e:
        print(f"Error connecting to Weaviate: {e}")

    return None



if __name__ == "__main__" :
    client = init_client(str(EMBED_MODEL_NAME))
    if isinstance(client, weaviate.WeaviateClient): 
        vector_store = WeaviateVectorStore(
                weaviate_client= client,
                index_name= "LlamaIndex"
                ) 

        client.close()
