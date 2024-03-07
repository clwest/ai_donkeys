import os
from dotenv import load_dotenv
from pprint import pprint

import spacy
from services.logging_config import root_logger as logger
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.memory import ChatMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_openai_tools_agent

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")
tavily_api_key = os.getenv("TAVILY_API_KEY")

tools = [TavilySearchResults(max_results=1)]
model = ChatOpenAI(
    openai_api_key=openai_key, model="gpt-4-0125-preview", temperature=0.2
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
        ),
        MessagesPlaceholder(variable_name="chat_history"),  
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


agent = create_openai_tools_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

chat_history_chain = ChatMessageHistory()

conversational_agent_extractor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: chat_history_chain,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
)

intro = conversational_agent_extractor.invoke(
    {"input": "I'm Donkey!"},
    {"configurable": {"session_id": "unused"}},
)

pprint(intro)
