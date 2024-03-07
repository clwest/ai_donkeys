import os
from dotenv import load_dotenv
from pprint import pprint

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

search = DuckDuckGoSearchRun()

template = """Turn the following user input into a search query for a search engine:
{input}"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()

chain = prompt | model | StrOutputParser() | search

sports = chain.invoke({"input": "Sports books."})

pprint(sports)