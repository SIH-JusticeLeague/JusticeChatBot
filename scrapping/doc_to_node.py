import os
import pickle
from llama_index.core.readers import Document
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.node_parser import MarkdownNodeParser, MarkdownElementNodeParser
from llama_index.core.schema import TextNode, BaseNode

def save_node_from_doc (doc_dir : str, node_dir : str) -> None | list[Document] | list[BaseNode]:
    doc_content = os.listdir(doc_dir)
    doc_list = []

    # maek document list in the memory
    for content in doc_content : 
        file_path = os.path.join(doc_dir, content)
        try : 
            with open (file_path, "rb") as f : 
                try : 
                    doc_list.append(pickle.load(f))
                except EOFError as e : 
                    print(e)
        except Exception as e:
            print(e)

    print (f"{len(doc_content)} documents read from {doc_dir}")

    return doc_list

    # Node parsing 
    try : 
        node_parser = MarkdownNodeParser(include_metadata= True, include_prev_next_rel= False)
        nodes = node_parser.get_nodes_from_documents(doc_list, show_progress= True)
    except Exception as e: 
        raise e
    
    print (f"{len(nodes)} nodes created")

    # persisting nodes using Document Store
    # document_store = SimpleDocumentStore()

    # saving list[BaseNode] to node_dir
    with open(os.path.join(node_dir, "nodes.pkl") , "wb") as f : 
        pickle.dump(nodes, f)

    print(f"nodes saved to {node_dir} as nodes.pkl")

    return None



if __name__ == "__main__" :
    doc_dir = os.path.join(os.getcwd(), "scrapped-data/doc-bin")
    node_dir = os.path.join(os.getcwd(), "scrapped-data")
    print(node_dir)
    save_node_from_doc(doc_dir,node_dir)
    pass
