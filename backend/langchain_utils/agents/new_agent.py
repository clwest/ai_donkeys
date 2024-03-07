import os
import logging
from dotenv import load_dotenv
from langchain.agents.tools import Tool
from langchain.agents import tool
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.tools import WikipediaQueryRun, ArxivQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from factory.token_factory import TokenCounterFactory
from services.logging_config import root_logger as logger
from chatbots.retrieval.chat_retrieval import ChatRetrievalLLM


load_dotenv()
openai_key = os.getenv("OPENAI_API")
connection_string = os.getenv("DEV_DATABASE_URL")

chat = ChatOpenAI(
    verbose=True,
    model="gpt-4-1106-preview",
    temperature=0.3,
    openai_api_key=openai_key,
)

arvix = ArxivQueryRun()
search = DuckDuckGoSearchAPIWrapper()
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
llm = OpenAI(temperature=0.8, openai_api_key=openai_key)
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_key)


@tool
def chat_retrieval_tool(query, formatted_chat_history, collection_name):
    """
    Wrapper function for ChatRetiervalLLM class.
    """
    chat_retrieval_llm = ChatRetrievalLLM()
    return chat_retrieval_llm.llm_query(query, formatted_chat_history, collection_name)


def query_pgvector(collection_name, query):
    vector_store = PGVector(connection_string, embeddings, collection_name)

    # Query the collection
    results = vector_store.similarity_search(query)

    # Process and display the results
    for result in results:
        print(result.page_content)


# Example usage
collection_name = "ethereum_netork "
query = "Who authored the Ethereuem Whitepaper?"
results = query_pgvector(collection_name, query)

logger.info(f"Results of the query: {results}")


# vectorstore = PGVector(
#     collection_name="langchain_pg_embeddings",
#     connection_string=CONNECTION_STRING,
#     embedding_function=embeddings,
# )

# # Initialize the language model
# llm = ChatOpenAI(
#     model="gpt-4-1106-preview",
#     temperature=0.3,
#     openai_api_key=openai_key,
# )

# query = "How does the Fuel network operate?"

# result = vectorstore.similarity_search(query)
# logger.info(f"Output of the result: {result}")


# agent = initialize_agent(
#     tools=[vectorstore],
#     llm=llm,
#     agent=AgentType.SIMILARITY_SEARCH,
#     verbose=True,
# )

# # Use the agent
# agent_executor = AgentExecutor(agent=agent, tools=[vectorstore])
# result = agent_executor.invoke({"query": "What is Fuel?"})
# pprint(result)
