import dotenv
import os

from weaviate import (
        WeaviateClient,
        connect_to_custom
        )

from llama_index.vector_stores.weaviate import WeaviateVectorStore 

# loading environmental variables 
dotenv.load_dotenv()
HUGGING_FACE_KEY = os.getenv("HUGGING_FACE_KEY")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")


# create client
def init_client(embed_model: str) -> WeaviateClient | None: 
    if not HUGGING_FACE_KEY:
        raise ValueError("HUGGING_FACE_KEY is not set in the environment variables.")

    if embed_model.split('/') != "sentence-transformers":
        embed_model = "sentence-transformers/" + embed_model

    # client init
    client = connect_to_custom(
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

    return client



if __name__ == "__main__" :
    client = init_client(str(EMBED_MODEL_NAME))
    if isinstance(client, WeaviateClient): 
        vector_store = WeaviateVectorStore(
                weaviate_client= client,
                index_name= "WeaviateVectorStore"
                ) 

        client.close()
