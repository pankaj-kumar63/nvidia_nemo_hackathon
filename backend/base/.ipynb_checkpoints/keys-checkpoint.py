import os 
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.memory import ConversationBufferMemory
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
import asyncio
# Load environment variables
nvidia_api_key = "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"
tavily_api_key = "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"
langchain_api_key = "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"

os.environ["NVIDIA_API_KEY"] = nvidia_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key

# Initialize LLM and Memory
def model_memory():
    llm = ChatNVIDIA(model="meta/llama-3.1-405b-instruct",max_tokens=2000)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return llm, memory

    



