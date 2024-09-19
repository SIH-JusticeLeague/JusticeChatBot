import dotenv
import os

from llama_index.core import(
        Settings,   
        StorageContext
        )
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.memory import ChatMemoryBuffer

# storage 
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.storage.index_store.redis import RedisIndexStore
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.chat_store.redis import RedisChatStore

from llama_index.llms.huggingface import HuggingFaceLLM, HuggingFaceInferenceAPI
from transformers import AutoTokenizer, BitsAndBytesConfig
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from database.vector_db import vector_db
from database.index_db import index_db
from database.document_db import document_db
from database.chat_db import chat_db

from torch import float16
# import torch


# loading environmental variables 
dotenv.load_dotenv()
HUGGING_FACE_KEY = os.getenv("HUGGING_FACE_KEY")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")
LLM = os.getenv("LLM")
TOKEN_LIMIT = int(os.getenv("TOKEN_LIMIT"))

assert isinstance(TOKEN_LIMIT, int) , "Environment Variable TOKEN_LIMIT must be an INTEGER"


node_parser = MarkdownNodeParser(
        include_metadata=True,
        include_prev_next_rel=True
        )
print(f"Node Parser : {node_parser.__repr_name__()}")
# setting global node parser
Settings.text_splitter = node_parser



# setting global settings 
# ----------------------------------------------------
if not EMBED_MODEL_NAME : 
    raise ValueError("EMBED_MODEL_NAME is not set in the environment variables")

# setting global embedding model
print(f"Embedding Model : {str(EMBED_MODEL_NAME)}")
Settings.embed_model = HuggingFaceEmbedding(str(EMBED_MODEL_NAME))



if not LLM : 
    raise ValueError("LLM is not set in the environment variables")

print(f"LLM and Tokenizer: {str(LLM)}")

# quantization 
quantization_config = BitsAndBytesConfig(
        load_in_4bit= True,
        bnb_4bit_compute_dtype= float16,
        bnb_4bit_quant_type= "nf4",
        bnb_4bit_use_double_quant=True
)

# setting global LLM 
Settings.llm = HuggingFaceInferenceAPI(
    model_name= str(LLM),
    tokenizer_name=str(LLM),
    context_window=4096,
    # max_new_tokens=256,
    model_kwargs={"quantization_config": quantization_config},
    generate_kwargs={"temperature": 0.1, "top_p": 0.9},
    # messages_to_prompt=messages_to_prompt,
    # completion_to_prompt=completion_to_prompt,
    device_map="auto",
) 

# setting global tokenizer
Settings.tokenizer = AutoTokenizer.from_pretrained(str(LLM))



# setting global transformation

storage_context = StorageContext.from_defaults(
        # setting global Vector Store
        vector_store = WeaviateVectorStore(
                        weaviate_client= vector_db.init_client(str(EMBED_MODEL_NAME)),
                        index_name= "WeaviateVectorStore"
                        ),
        # setting global Index Store
        index_store= RedisIndexStore(
                        redis_kvstore= index_db.init_client(),
                        namespace= "RedisIndexStore"
                        ),
        # setting global Document Store
        docstore = RedisDocumentStore(
                        redis_kvstore= document_db.init_client(),
                        namespace= "RediDocumentStore"
                        )
        )

chat_memory = ChatMemoryBuffer.from_defaults(
        # setting global Chat Store
        chat_store= RedisChatStore(
                        redis_client= chat_db.init_client()
                        ),
        token_limit= TOKEN_LIMIT
        )


print("Gobal config finished setup ...")

# setting global prompt format

# setting global retrieval format

# setting global print format

if __name__ == "__main__" :
    pass 
