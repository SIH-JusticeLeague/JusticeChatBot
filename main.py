import os
from pprint import pprint
from global_config import *
from scrapping import doc_to_node 
from llama_index.core import(
        Document, 
        VectorStoreIndex,
        load_indices_from_storage,
        ) 

from llama_index.vector_stores.weaviate import WeaviateVectorStore
import time


if __name__ == "__main__" : 
    # initializing vector database

    # doc_dir = os.path.join(os.getcwd(), "scrapped-data/doc-bin")
    # node_dir = os.path.join(os.getcwd(), "scrapped-data")
    # doc_list = doc_to_node.save_node_from_doc(doc_dir, node_dir)

    # if isinstance(doc_list, list): 
    #     assert isinstance(doc_list[0], Document) , "cannot get doc_list" print("\nbuilding index\n")
    #     start = time.time()
    #     index = VectorStoreIndex.from_documents(
    #             doc_list, 
    #             show_progress= True, 
    #             # storage_context= storage_context
    #             )
    #     end = time.time()
    #     print(f"built in {(end-start)%60} minutes")
    #     print(index)

    __import__('pprint').pprint(storage_context)

    vector_store = 
    index_store = VectorStoreIndex.from_vector_store()
    pprint(vector_store)
