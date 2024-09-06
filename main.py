from settings.global_config import *
from scrapping import doc_to_node 
from llama_index.core import Document, VectorStoreIndex
import time


if __name__ == "__main__" : 
    # initializing vector database

    doc_dir = os.path.join(os.getcwd(), "scrapped-data/doc-bin")
    node_dir = os.path.join(os.getcwd(), "scrapped-data")
    doc_list = doc_to_node.save_node_from_doc(doc_dir, node_dir)

    if doc_list : 
        assert isinstance(doc_list[0], Document) , "cannot get doc_list"
        print("\nbuilding index\n")
        start = time.time()
        index = VectorStoreIndex.from_documents(
                doc_list, 
                show_progress= True, 
                # storage_context= storage_context
                )
        end = time.time()
        print(f"built in {(end-start)%60} minutes")
        print(index)




