import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

def get_company_info_retriever():
    """
    Loads company data from company_data.txt and creates a simple FAISS retriever.
    Uses local HuggingFace Embeddings (free, no API key required).
    """
    # 1. Load the data
    BASE_DIR = os.path.dirname(__file__)
    data_path = os.path.join(BASE_DIR, "company_data.txt")
    loader = TextLoader(data_path)
    documents = loader.load()

    # 2. Split into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # 3. Create local embeddings and vector store
    # Using a small, fast model: all-MiniLM-L6-v2
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 4. Return as a retriever
    return vectorstore.as_retriever()
