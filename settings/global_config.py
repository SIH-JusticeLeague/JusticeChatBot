import dotenv
import os

from llama_index.core import(
        Settings,   
        StorageContext
        )
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.vector_stores.weaviate import WeaviateVectorStore

from llama_index.llms.huggingface import HuggingFaceLLM
from transformers import AutoTokenizer, BitsAndBytesConfig
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from vector_store.weaviate import init_client


# to avoiding warning
from pydantic._internal import _fields, _config
_fields.model_config['protected_namespaces'] = ()

# loading environmental variables 
dotenv.load_dotenv()
HUGGING_FACE_KEY = os.getenv("HUGGING_FACE_KEY")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")
LLM = os.getenv("LLM")



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

# setting global LLM 
Settings.llm = HuggingFaceLLM(
    model_name= str(LLM),
    tokenizer_name=str(LLM),
    context_window=8192,
    # max_new_tokens=256,
    # model_kwargs={"quantization_config": quantization_config},
    generate_kwargs={"temperature": 0.1, "top_p": 0.9},
    # messages_to_prompt=messages_to_prompt,
    # completion_to_prompt=completion_to_prompt,
    device_map="auto",
) 

# setting global tokenizer
Settings.tokenizer = AutoTokenizer.from_pretrained(str(LLM))



# setting global transformation


# setting gloabl Document Store
# setting global Chat Store
storage_context = StorageContext.from_defaults(
        # setting global Vector Store
        vector_store = WeaviateVectorStore(
                        weaviate_client= init_client(str(EMBED_MODEL_NAME)),
                        index_name= "WeaviateIndex"
                        ) 
        )

# setting global prompt format

# setting global retrieval format

# setting global print format
