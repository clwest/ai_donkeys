import logging
import os
from pprint import pprint
from dotenv import load_dotenv
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


prompt = PromptTemplate(input_variables=["query"], template="{query}")

llm_chain = LLMChain(llm=llm, prompt=prompt)


with app.app_context():
    engine = db.engine
    datebase = SQLDatabase(engine=engine)
    sql_chain = SQLDatabaseChain(database=datebase, llm_chain=llm_chain, verbose=True)

    sql_agent = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=datebase, llm=llm),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        # max_iterations=3,
    )
    token_counter_factory = TokenCounterFactory()
    token_counter = token_counter_factory.create_token_counter(sql_agent)

    result = token_counter(
        "What are some topics that we have had a conversation about?",
    )
