import dotenv
import os
from llama_index.core import VectorStoreIndex 
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import AutoTokenizer, BitsAndBytesConfig
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core.node_parser import MarkdownNodeParser


# loading environmental variables 
dotenv.load_dotenv()
HUGGING_FACE_KEY = os.getenv("HUGGING_FACE_KEY")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")
LLM = os.getenv("LLM")

# setting global settings 
if not EMBED_MODEL_NAME : 
    raise ValueError("EMBED_MODEL_NAME is not set in the environment variables")
Settings.embed_model = HuggingFaceEmbedding(str(EMBED_MODEL_NAME))

if not LLM : 
    raise ValueError("LLM is not set in the environment variables")
Settings.tokenizer = AutoTokenizer.from_pretrained(str(LLM))

Settings.text_splitter = MarkdownNodeParser()

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


