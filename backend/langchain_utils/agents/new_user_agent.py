import os
import logging
from pprint import pprint
from dotenv import load_dotenv

from langchain.agents import (
    AgentExecutor,
    AgentType,
    initialize_agent,
    load_tools,
    create_sql_agent,
)
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, LLMCheckerChain
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    MessagesPlaceholder,
)
from langchain.prompts.chat import ChatPromptValue
from langchain.tools.vectorstore.tool import VectorStoreQATool
from langchain.utilities import WikipediaAPIWrapper, SQLDatabase
from langchain.vectorstores import Pinecone
from langchain_core.messages import SystemMessage
from factory import create_app, db
from factory.pinecone_factory import init_pinecone
from factory.token_factory import TokenCounterFactory
from factory.lg_db_factory import create_lg_database

# Load environment variables
load_dotenv()
init_pinecone()

# Pinecone and OpenAI API configuration
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")

# Initialize ChatOpenAI and Conversation Memory
chat = ChatOpenAI(
    verbose=True,
    model="gpt-4-1106-preview",
    temperature=0.3,
    openai_api_key=openai_api,
)
memory = ConversationSummaryMemory(
    llm=chat, memory_key="chat_history", k=5, return_messages=True
)

system_template = """You are a helpful assistant that is extremely knowledgeable about blockchain technologies and Web3 projects, 
                    including Ethereum, Stacks, and Fuel networks. Please provide detailed and accurate answers to user queries. 
                    Use available data and resources to inform your responses. 
                    Do not lie or make up answers, if you do not know the answer simply reply 
                     'I don't know the answer can you please provide more information?'.
                  """

# Chat Template for Blockchain Knowledge
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template("{user_query}"),
    ]
)


# Agent and SQL Chain Setup

app = create_app()
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api)
vectorstore = Pinecone.from_existing_index(embedding=embeddings, index_name=index_name)

prompt = PromptTemplate(input_variables=["query"], template="{query}")
llm_chain = LLMChain(llm=chat, prompt=prompt, memory=memory)

lg_data = create_lg_database()

sql_chain = SQLDatabaseChain(database=lg_data, llm_chain=llm_chain, verbose=True)
sql_agent = create_sql_agent(
    llm=chat,
    toolkit=SQLDatabaseToolkit(db=lg_data, llm=chat),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

token_counter_factory = TokenCounterFactory()
token_counter = token_counter_factory.create_token_counter(sql_agent)
results = token_counter("Can you please remind me again how Slither works?")
pprint(f"Token counter results: {results}")
