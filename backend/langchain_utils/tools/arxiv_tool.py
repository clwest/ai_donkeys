import logging
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
openai_api = os.getenv("OPENAI_API")

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(temperature=0, openai_api_key=openai_api)
tools = load_tools(
    ["arxiv"],
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

poker = agent_chain.run("How can Blockchain technology return privacy to users?")
print(poker)
