import pickle
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from timeit import default_timer as timer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext, VectorStoreIndex

with open("custom_prompt.pkl", "rb") as file:
    custom_template=pickle.load(file)
    
with open("tree_index_list.pkl","rb") as f:
    tree_index_list=pickle.load(f)

with open("chapter_index.pkl","rb") as f:
    chapter_index=pickle.load(f)
    
with open("index_dict.pkl", "rb") as file:
    index_dict=pickle.load(file)

conversation_prompt=ChatPromptTemplate.from_template(template=custom_template)
    
#with open("prompt_engg.pkl", "rb") as file:
#    prompt_engg=pickle.load(file)

#prompt_query=ChatPromptTemplate.from_template(template=prompt_engg)

embedding_function = HuggingFaceEmbedding(model_name="sentence-transformers/all-roberta-large-v1")

def select_index(index, index_dict=index_dict, embedding_function=embedding_function):
    for key in index_dict:
        if index==key:
        
            qdrant_local_path = index_dict[key]
            qdrant_client = QdrantClient(path=qdrant_local_path)
            collection_name = key
            vector_size = 1024
            qdrant_vector_store = QdrantVectorStore(client=qdrant_client, collection_name=collection_name)
            storage_context = StorageContext.from_defaults(vector_store=qdrant_vector_store)
            vector_index = VectorStoreIndex.from_vector_store(vector_store=qdrant_vector_store, embed_model=embedding_function)
            
            return vector_index

