import logging
import os
from pprint import pprint
from dotenv import load_dotenv
from langchain.tools.vectorstore.tool import VectorStoreQATool
from langchain.agents import AgentExecutor, AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.agents import load_tools
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from langchain.llms import OpenAI
from factory import create_app

from factory.pinecone_factory import init_pinecone
from factory import db
from factory.token_factory import TokenCounterFactory
from langchain.memory import ConversationBufferMemory
from langchain.docstore import Wikipedia
from langchain.agents.react.base import DocstoreExplorer, Tool

memory = ConversationBufferMemory(memory_key="chat_history")

load_dotenv()
init_pinecone()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api)
app = create_app()
vectorstore = Pinecone.from_existing_index(embedding=embeddings, index_name=index_name)


llm = ChatOpenAI(
    verbose=True,
    model="gpt-4-1106-preview",
    temperature=0.3,
    openai_api_key=openai_api,
)


# llm = OpenAI(openai_api_key=openai_api, temperature=0)


tools = load_tools(["llm-math"], llm=llm)

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
)

# math = zero_shot_agent("what is (4.5*2.1)^2.2?")


prompt = PromptTemplate(input_variables=["query"], template="{query}")

llm_chain = LLMChain(llm=llm, prompt=prompt)


# reinitialize the agent
conversational_agent = initialize_agent(
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    memory=memory,
)

token_counter_factory = TokenCounterFactory()
token_counter = token_counter_factory.create_token_counter(conversational_agent)

# result = token_counter(
#     "Can you please give a detailed explanation of how DeFi works on different blockchains?",
# )

wiki = DocstoreExplorer(Wikipedia())
tools = [
    Tool(name="Search", func=wiki.search, description="search wikipedia"),
    Tool(name="Lookup", func=wiki.lookup, description="lookup a term in wikipedia"),
]

docstore_agent = initialize_agent(
    tools, llm, agent="react-docstore", verbose=True, max_iterations=3
)


with app.app_context():
    # sql_chain = SQLDatabaseChain(llm=llm, datebase=db, verbose=True)
    engine = db.engine
    datebase = SQLDatabase(engine=engine)
    sql_chain = SQLDatabaseChain(database=datebase, llm_chain=llm_chain, verbose=True)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=datebase, llm=llm),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    result = token_counter(
        "What date and time was the last custom question and the response from the ai?",
    )
