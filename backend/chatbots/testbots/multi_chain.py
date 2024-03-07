import os
from dotenv import load_dotenv
from pprint import pprint

import spacy
from services.logging_config import root_logger as logger
from operator import itemgetter
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

model = ChatOpenAI(verbose=True)


prompt1 = ChatPromptTemplate.from_template(
    "generate a {attribute} color. Return the name of the color and nothing else:"
)

prompt2 = ChatPromptTemplate.from_template(
    "what is a fruit color: {color}. Return the name of the fruit and nothing else:"
)

prompt3 = ChatPromptTemplate.from_template(
    "what is a country with a flag that has the color: {color}. Return the name of the country and nothing else:"
)

prompt4 = ChatPromptTemplate.from_template(
    "What is the color of {fruit} and the flag of {country}?"
)

model_parser = model | StrOutputParser()

color_generator = (
    {"attribute": RunnablePassthrough()} | prompt1 | {"color": model_parser}
)

color_to_fruit = prompt2 | model_parser

color_to_country = prompt3 | model_parser

question_generator = (
    color_generator | {"fruit": color_to_fruit, "country": color_to_country} | prompt4
)

ask = question_generator.invoke("grass")
prompt = model.invoke(ask)
pprint(prompt)