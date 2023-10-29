from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings
import qdrant_client
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.schema import retriever
import streamlit as st



def get_answer(prompt):
# create a qudrant client
    QDRANT_HOST = st.secrets["QDRANT_HOST"]
    QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    QDRANT_COLLECTION_NAME = st.secrets["QDRANT_COLLECTION_NAME"]
    

    client = qdrant_client.QdrantClient(
        url = QDRANT_HOST, 
        api_key = QDRANT_API_KEY
    )
    
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = Qdrant(
    client=client, 
    collection_name=QDRANT_COLLECTION_NAME, 
    embeddings=embeddings,
    )
    
    qa = RetrievalQA.from_chain_type(
        llm = OpenAI(),
        chain_type='stuff',
        retriever = vector_store.as_retriever()
    )
    
    response = qa.run(prompt)
    return response

