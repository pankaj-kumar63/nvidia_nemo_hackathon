import os
import sqlite3
from langchain.chains import LLMChain
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from base.prompt import prompt_with_data, prompt_without_data,prompt_with_memory_history
from nemoguardrails import LLMRails, RailsConfig
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import List, Callable, Any
from langchain_core.pydantic_v1 import BaseModel, Field
from base.prompt import prompt_with_route_query,prompt_with_TavilySearchInput,prompt_with_query_correction
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from base.keys import nvidia_api_key,tavily_api_key,langchain_api_key,model_memory
import sys 
import os
from base.vector_store import create_db, store_report, retrieve_data
import json
import asyncio
import os
import glob
from datetime import datetime



os.environ["NVIDIA_API_KEY"] = nvidia_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key

llm,memory=model_memory()
embedder = NVIDIAEmbeddings()
    
# # Variable to keep track of initialization state

initialized = False

# Function to return the current value of 'initialized'
async def value() -> bool:
    """
    Asynchronously retrieves the current state of the 'initialized' flag.

    This function checks the global variable 'initialized', which indicates whether 
    the chatbot has been initialized with the student-specific data. 

    Returns:
        bool: The current value of the 'initialized' flag. 
              Returns True if the chatbot is initialized; otherwise, returns False.

    Notes:
        - The 'initialized' flag is intended to track whether student-specific data 
          has been fetched and stored during the chatbot session.
    """
    global initialized
    print("Value function initialized", initialized)
    return initialized

# Load sample exam data
async def data() -> str:
    """
    Asynchronously loads and returns the contents of a sample exam data file (sample.json) as a string.

    This function opens the 'sample.json' file in read mode, reads its contents, 
    and returns the entire data as a string. It is designed to handle asynchronous operations.

    Returns:
        str: The contents of the 'sample.json' file as a string.
    """
 
    # Define the folder path
    folder_path = '/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/quiz_answers'
    
    # Get the list of all files in the folder
    files = glob.glob(os.path.join(folder_path, '*'))
    
    # Check if the folder contains any files
    if files:
        # Get the latest file based on creation or modification time
        latest_file = max(files, key=os.path.getctime)
    
        # Get the file name from the full path
        file_name = os.path.basename(latest_file)
    
        # Get the creation time of the latest file
        creation_time = os.path.getctime(latest_file)
    
        # Convert the timestamp to a readable format (date and time)
        creation_date_time = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
    
        # Print the latest file name and its creation date & time
        print(f"Latest file: {file_name}")
        print(f"Created on: {creation_date_time}")
    
        # Open the latest file using the full path
        with open(os.path.join(folder_path, file_name), "r") as outfile:
            data = json.load(outfile)
        
        return data
        

async def student_id() -> str:
    """
    Reads the student ID from a file asynchronously.

    This function opens a file named 'file.txt', reads its contents (which contains 
    the Student_Id), and returns the ID as a string. The file is read in a 
    synchronous manner, but the function can be integrated within an asynchronous flow.

    Returns:
        str: The student ID read from the file.
    """
    with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/file.txt", 'r') as file:
        Email_Id = file.read()
    print(Email_Id)
    return Email_Id





async def student_data(query: str, data: str,Email_Id:str) -> str:
    
    """
    Asynchronously handles the retrieval of student-specific data and generates a response using 
    an LLM (Large Language Model) based on the student's current and historical exam data.

    This function retrieves any existing report for the student using the provided `Student_Id`. 
    If no previous report is found, it generates a response based only on the provided query 
    and data. If a previous report exists, it incorporates that report into the response.

    Args:
        query (str): The query or question provided by the student.
        data (str): The current exam data or additional context for the student's performance.
        Student_Id (int): The unique identifier of the student used to retrieve previous reports.

    Returns:
        str: The generated response from the LLM based on the student's data and query.

    Workflow:
        1. Retrieve the old report of the student using `Student_Id`.
        2. If no old report exists, the LLM generates a response based on the `query` and `data`.
        3. If an old report exists, it is incorporated into the prompt, and the response is generated accordingly.
    """
    final_prompt_with_data = ChatPromptTemplate.from_messages(
                            messages=[
                                    MessagesPlaceholder(variable_name="chat_history"),
                                    HumanMessagePromptTemplate.from_template(prompt_with_data)])

    conversation_chain_with_data = LLMChain(
                                    llm=llm,
                                    prompt=final_prompt_with_data,
                                    memory=memory)
    #Sudent old report 
    student_old_report=retrieve_data(Email_Id)
    if student_old_report is None:
        input_text = f"Question: {query}\nData: {data}\ntotal_question_data:{len(data)}"
        # print("input_text\n", input_text)
        response = await conversation_chain_with_data.arun({"input_text": input_text})
    else:
        input_text = f"Question: {query}\nData: {data}\ntotal_question_data:{len(data)}\nold_report: {student_old_report}"
        # print("input_text\n", input_text)
        response = await conversation_chain_with_data.arun({"input_text": input_text})
    
    return response



# Initialize vector store retriever (Chroma)
async def retriever(query: str) -> list:

    """
    Asynchronously retrieves relevant documents from the vector store based on the provided query 
    using the Chroma vector database.

    This function initializes a Chroma vector store, which uses an embedding function to 
    encode and retrieve documents. The retriever fetches the top `k` relevant documents 
    (in this case, 10) based on the similarity of the query to the stored embeddings.

    Args:
        query (str): The input query for which relevant documents need to be retrieved.

    Returns:
        list: A list of relevant documents retrieved from the vector store based on the query.

    Workflow:
        1. Initialize the Chroma vector store using the specified embedding function and persist directory.
        2. Use the vector store as a retriever to search for the top 10 relevant documents.
        3. Print the relevant documents for debugging purposes.
        4. Return the list of relevant documents.

    Note:
        - The `embedder` used in the function is assumed to be an instance of a pre-defined embedding model.
        - The vector store persists in the directory "Neet_vector_store".
    """
    path="/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/Neet_vector_store"
    vectorstore = Chroma(
                  embedding_function=embedder,
                  persist_directory=path)
    
    retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
    contexts = retriever.get_relevant_documents(query)
    return contexts
     

# Chain to execute RAG (without student-specific data)
async def execute_rag(query: str, contexts:list) -> str:

    """
    Asynchronously generates a response using a Retrieval-Augmented Generation (RAG) 
    approach without using student-specific data. 

    This function takes a query and relevant contexts (retrieved documents) as input, 
    and uses an LLM (Large Language Model) to generate a response based on the combined 
    information. It does not include any student-specific historical data.

    Args:
        query (str): The user's input question or query.
        contexts (list): A list of relevant contexts or documents retrieved from the vector store.

    Returns:
        str: The generated response from the LLM based on the query and provided contexts.

    Workflow:
        1. Create a prompt template using `prompt_without_data` for conversation history 
           and user input.
        2. Initialize the conversation chain using the LLM and memory for chat history.
        3. Combine the query and contexts into a formatted input text.
        4. Generate and return the response using the conversation chain.
    """
    final_prompt_without_data = ChatPromptTemplate.from_messages(
                                messages=[
                                    HumanMessagePromptTemplate.from_template(prompt_without_data)])

    conversation_chain_without_data = LLMChain(
                                                llm=llm,
                                                prompt=final_prompt_without_data,
                                                )
    
    input_text = f"Question: {query}\nContext: {contexts}"
    response = await conversation_chain_without_data.arun({"input_text": input_text})
  
        
    return response



async def memory_agent_query(query: str) -> str:

    """
    Asynchronously retrieves information from stored memory based on a user query, utilizing a language model with memory       capabilities.

    This function sets up a conversation chain that leverages a memory buffer containing performance reports and associated     prompts.
    Given a user's query, it constructs an input text that includes the query and data retrieved from memory, then passes       it through the conversation chain.
    The function returns a response containing information directly related to the query, based on the retrieved memory         data.

    Args:
        query (str): The user's specific question or request regarding a student's performance report or other stored data.

    Returns:
        str: The response generated by the language model, containing the information relevant to the user's query or                    indicating if no matching data is found.

    Raises:
        ValueError: If there are missing keys or inputs required for the conversation chain to function properly.

    Example:
        response = await memory_agent_query("How many questions did I answer correctly in the given exam?")
    """
    final_prompt_memory_history = ChatPromptTemplate.from_messages(
                                    messages=[
                                        MessagesPlaceholder(variable_name="chat_history"),
                                        HumanMessagePromptTemplate.from_template(prompt_with_memory_history)])

    conversation_chain_with_memory = LLMChain(
                                    llm=llm,   
                                    prompt=final_prompt_memory_history,
                                    memory=memory)  
    
    memory_data=memory.load_memory_variables({})
    input_text=f"query:{query}/n memory_data:{memory_data}"
    #Run the conversation chain asynchronously
    response = await conversation_chain_with_memory.arun({"input_text": input_text})
    return response

async def classification_query(query: str) -> str:
    """
    Asynchronously processes a given query to classify it using a pre-defined language model and prompt template.

    This function leverages a conversation chain powered by a language model (LLM) to classify the provided query. 
    The chain is instantiated with a prompt template (`prompt_with_route_query`) that structures the query and 
    any chat history, along with memory management to retain context across queries.

    Args:
        query (str): The input query that needs to be classified.

    Returns:
        str: The classified result based on the provided query.
    
    Workflow:
    1. The function first creates a final prompt using `ChatPromptTemplate`, which incorporates a placeholder for 
       chat history and a template (`prompt_with_route_query`) for structuring the query.
    2. A conversation chain is instantiated using the specified LLM, the created prompt, and a memory object 
       to maintain context.
    3. The query is passed to the conversation chain's `arun` method for asynchronous execution.
    4. The classification result is printed to the console and returned.

    Note:
        - This function assumes that `prompt_with_route_query`, `llm`, and `memory` are defined and available in the 
          broader scope.
        - `arun` is an asynchronous method that handles the execution of the conversation chain.
    """
    # Assuming `prompt_with_route_query` is defined and accessible
    final_prompt = ChatPromptTemplate.from_messages(
        messages=[
            HumanMessagePromptTemplate.from_template(prompt_with_route_query)])
    
    # Instantiate the conversation chain with the specified LLM, prompt, and memory
    conversation_chain = LLMChain(
                            llm=llm,
                            prompt=final_prompt)
    
    memory_data_class=memory.load_memory_variables({})
    input_text=f"query:{query}/n memory_data:{memory_data_class}"
    # Run the conversation chain asynchronously
    classification = await conversation_chain.arun({"input_text": input_text})
    
    # Output the classification result
    print(f"Query Classification: {classification}")
    
    return classification

def query_correction(query:str) ->str:
    """
    Corrects the user's query for grammar and clarity, ensuring it is suitable for processing in either a vector store,        memory store, or internet search.

    This function uses an LLM chain with a predefined prompt to correct the user's input. The corrected query is returned      in a clean, refined format.

    Args:
        query (str): The user's original query, typically related to NEET Biology for Class 11 and 12 NCERT books, general         questions, or internet searches.

    Returns:
        str: The corrected version of the query, refined for clarity and directed to the appropriate resource.

    Steps:
        1. A prompt template is created using `ChatPromptTemplate.from_messages()`, which includes instructions and                   examples for query correction.
        2. A conversation chain is initialized using `LLMChain` with the specified LLM and prompt.
        3. The user's input query is processed through the chain.
        4. The corrected query is stripped of any extraneous text and returned.

    Example:
        Input: "classification bio class 11"
        Output: "Explain the biological classification from Class 11 NCERT Biology."
    """
    # Create the final prompt template
    final_prompt_query_correction = ChatPromptTemplate.from_messages(
                                    messages=[
                                        HumanMessagePromptTemplate.from_template(prompt_with_query_correction)])
    
    # Initialize the conversation chain
    conversation_chain_query_correction = LLMChain(
                                    llm=llm,  
                                    prompt=final_prompt_query_correction)
    
    answer = conversation_chain_query_correction.run({"query": query})
    query=answer.strip()
    # Output only the corrected query
    return query

# Handle Internet Search if classified as "internet search"
async def int_search(query: str)-> str:
    """
    Handles internet search queries classified as "internet search" using the TavilySearchResults API.

    This function sets up the Tavily search tool to fetch relevant document snippets from the internet.
    It defines the schema for the search input, creates a ReAct agent for handling the search, and executes
    the search based on the provided input.

    Args:
        input_text (str): The user's query that needs to be searched on the internet.

    Returns:
        str: The search results in the form of relevant document snippets retrieved from the internet.
    
    Steps:
        1. Initializes the `TavilySearchResults` tool for internet search.
        2. Defines the schema for the search input using `TavilySearchInput`.
        3. Creates a ReAct agent with a prompt using the search tool.
        4. Executes the agent to retrieve search results based on the user's query.
        5. Returns the output containing the search results.
    """
    internet_search = TavilySearchResults()
    internet_search.name = "internet_search"
    internet_search.description = "Returns a list of relevant document snippets for a textual query retrieved from the           internet."

    class TavilySearchInput(BaseModel):
        query: str = Field(description="Query to search the internet with")

    internet_search.args_schema = TavilySearchInput
   
    # Create ReAct Agent
    react_prompt = ChatPromptTemplate.from_template(prompt_with_TavilySearchInput)
    agent = create_react_agent(llm, tools=[internet_search], prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[internet_search], verbose=True,handle_parsing_errors=True)

    # Execute Agent and Return Response
    
    response = agent_executor.invoke({"input": query})
    return response['output']



async def chat(question, flag):
    print("Flag inside t2", flag)
    """
    Implements an interactive NEET Exam Analysis Chatbot that handles user queries and 
    generates responses using Retrieval-Augmented Generation (RAG) or student-specific data.

    Args:
        question (str): The user's question to the chatbot.

    Returns:
        Response from the LLM.
    """
    global initialized
    initialized = flag

    # Initialize Nemoguardrails configuration
    config = RailsConfig.from_path("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/Config")
    rag_rails = LLMRails(config)

    # Register actions
    rag_rails.register_action(action=data, name="data")
    rag_rails.register_action(action=student_data, name="student_data")
    rag_rails.register_action(action=classification_query, name="classification_query")
    rag_rails.register_action(action=memory_agent_query, name="memory_agent_query")
    rag_rails.register_action(action=int_search, name="int_search")
    rag_rails.register_action(action=retriever, name="retriever")
    rag_rails.register_action(action=execute_rag, name="rag")
    rag_rails.register_action(action=value, name="value")
    rag_rails.register_action(action=student_id, name="student_id")

    # Handle student-specific data first, then switch to context-based retrieval
    if not initialized:
        print("Inside not initialized")
        with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/file.txt", 'r') as file:
            Email_Id = file.read()

        response = await rag_rails.generate_async(prompt=question)

        with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/report.txt", 'w') as f:
            f.write(response)

        store_report(Email_Id, response)  # Store the generated response
        initialized = True  # Set the initialized flag here
    else:
        question = query_correction(question)
        print(question)
        response = await rag_rails.generate_async(prompt=question)
        print(response)
    
    if initialized:
        with open("/hackathon_teams/hack_team_11/workspace/Nvidia_nim_hackathon/backend/base/response.txt", 'w') as f:
            f.write(response)

    return response

        
        




