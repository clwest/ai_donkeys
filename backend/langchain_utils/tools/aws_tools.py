from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI

import logging
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
openai_api = os.getenv("OPENAI_API")
aws_region = os.getenv("AWS_DEFAULT_REGION")


llm = OpenAI(temperature=0, openai_api_key=openai_api)

tools = load_tools(
    ["awslambda"],
    awslambda_tool_name="email-sender",
    awslambda_tool_description="sends an email with the specified content to test@testing123.com",
    function_name="testFunction1",
)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

email = agent.run("Send an email to test@testing123.com saying hello world.")
print(email)
