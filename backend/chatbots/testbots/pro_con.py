import os
from dotenv import load_dotenv
from pprint import pprint

import spacy
# from services.logging_config import root_logger as logger
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

planner = (
    ChatPromptTemplate.from_template("Generate an argument about: {input}")
    | ChatOpenAI()
    | StrOutputParser()
    | {"base_response": RunnablePassthrough()}
)

arguments_for = (
    ChatPromptTemplate.from_template(
        "List the pros or positive aspets of {base_response}"
    )
    | ChatOpenAI()
    | StrOutputParser()

)

arguments_against = (
    ChatPromptTemplate.from_template(
        "List the cons or negative aspeects of {base_response}"
    )
    | ChatOpenAI()
    | StrOutputParser()
)

final_responder = (
    ChatPromptTemplate.from_messages(
        [
            ("ai", "{original_response}"),
            ("human", "Pros:\n{results_1}\n\nCons:\n{results_2}"),
            ("system", "Generate a final response given the critique")  
        ]
    )
    | ChatOpenAI()
    | StrOutputParser()
)

chain = (
    planner
    | {
        "results_1": arguments_for,
        "results_2": arguments_against,
        "original_response": itemgetter("base_response"),
    }
    | final_responder
)

scrum = chain.invoke({"input": "Building a Start-up"})
pprint(scrum)