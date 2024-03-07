import os

import logging
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper
from factory import create_app, db
from factory.pinecone_factory import init_pinecone
from factory.token_factory import TokenCounterFactory
from factory.lg_db_factory import create_lg_database

load_dotenv()
init_pinecone()

# Pinecone and OpenAI API configuration
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")

llm = ChatOpenAI(
    verbose=True,
    model="gpt-4-1106-preview",
    temperature=0.3,
    openai_api_key=openai_api,
)

search = DuckDuckGoSearchRun()
wikipedia = WikipediaAPIWrapper()

search_tool = Tool(
    name="Web Search",
    func=search.run,
    description="A useful tool for searching the Internet to find information on world events, issues, ect. Useful using for general topics. Use precise questions.",
)

wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia.run,
    description="A useful tool for searching the Internet to find information on world events, issues, ect. Useful for general topics. Use precise questions.",
)

prompt = PromptTemplate(
    template="""Plan: {input}

  History: {chat_history}

  Let's think about the answer step by step
  If it's information retrieval task, solve it like a professor in a particlar field.""",
    input_variables=["input", "chat_history"],
)

plan_prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template="""Prepare plan for task execution. (e.g. retrieve current date to find weather forecast)
  Tools to use: wiki, web search

  REMEMBER: Keep in mind that you don't have information about current date, temperature, information after April 2023. Because of that you need to use tools to find them.

  Question: {input}

  History: {chat_history}

  Output looks like this:
  '''
    Question: {input}

    Execution plan: {execution_plan}

    Rest of needed information: [rest_of_needed_information]
  '''

  IMPORTANT: If there is no question, or plan is not needed (YOU HAVE TO DECIDE!), just
  populate {input} (pass it a result), The output should look like this:
  '''
    input: {input}
  '''
  """,
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

plan_chain = ConversationChain(
    llm=llm,
    memory=memory,
    input_key="input",
    prompt=plan_prompt,
    output_key="output",
)

agent = initialize_agent(
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    tools=[search_tool, wikipedia_tool],
    llm=llm,
    verbose=True,
    max_iterations=3,
    prompt=prompt,
    memory=memory,
)
