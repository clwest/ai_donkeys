import logging
import os
from pprint import pprint
from dotenv import load_dotenv

from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool

load_dotenv()
openai_api = os.getenv("OPENAI_API")


llm = ChatOpenAI(temperature=0, openai_api_key=openai_api)
tools = [YahooFinanceNewsTool()]

yahoo_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

btc = yahoo_chain.run("What happened with the Gamestop today?")
