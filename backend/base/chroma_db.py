from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import os
import chromadb
from langchain.vectorstores import Chroma
from prompt import prompt
from keys import nvidia_api_key,tavily_api_key,langchain_api_key
import nest_asyncio
nest_asyncio.apply()

os.environ["NVIDIA_API_KEY"] = nvidia_api_key
embedder = NVIDIAEmbeddings()


output_folder = '/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/Clean_Data_Neet'
vector_store_directory = "/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/Neet_vector_store"

# List all markdown files in the output folder
files = [f for f in os.listdir(output_folder) if f.endswith('.md')]
documents = []  # Collect documents here

# Iterate through each markdown file
for file in files:
    # Full path to the markdown file
    path = os.path.join(output_folder, file)
    
    # Load the markdown file for further processing
    loader = UnstructuredMarkdownLoader(path)
    loaded_documents = loader.load()
    # print(loaded_documents)
    
    # Extend the documents list with the content of loaded documents
    for doc in loaded_documents:
        documents.append(doc)

# Split the loaded documents into chunks for embedding
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
split_docs = text_splitter.split_documents(documents)

# Store the document embeddings in the Chroma vector store with persistence
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedder,
    persist_directory=vector_store_directory)  # Persist vector store for future use

# Persist the database
vectordb.persist()
