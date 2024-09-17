from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever, RecursiveRetriever
from llama_index.core import (
    get_response_synthesizer,
    PromptTemplate
)
from llama_index.core.response_synthesizers import TreeSummarize


prompt_format = PromptTemplate(
    "The context :\n"
    "{context_str}\n"
    "Given this information, please Answer the quesiton : {query_str}\n"
)  

class QueryEngine (CustomQueryEngine):
    retriever = RecursiveRetriever()
    # retriever = BaseRetriever()
    synthesizer = TreeSummarize()
    prompt_format = prompt_format

    def query (self, query_str : str):

        # Nodes list from Retriever
        assert(hasattr(self.retriever,"retrieve")), "check retriver attribute"
        nodes = self.retriever.retrieve(query_str)

        # building context string
        # assert(nodes is not None), "Nodes not retrieved"
        if nodes is None: 
            print("No Context Retrieved")
            context_str = ""
        else : 
            context_str = "\n".join([node.node.get_content() for node in nodes])


        # format retrieved data 
        assert(hasattr(self.prompt_format, "format")), "check prompt template"
        prompt = prompt_format.format(context_str= context_str, query_str=query_str)

        # Join retrieved data
        assert(hasattr(self.synthesizer,"synthesize")), "check synthesizer"


        

        # Response Obj from LLM call : 
        pass
