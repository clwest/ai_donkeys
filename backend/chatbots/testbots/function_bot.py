import os
from dotenv import load_dotenv
from pprint import pprint

import spacy
from services.logging_config import root_logger as logger
from operator import itemgetter

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

prompt = ChatPromptTemplate.from_template("tell me a joke about {foo}") 
model = ChatOpenAI(verbose=True)


functions = [
    {
        "name": "joke",
        "description": "A funny joke",
        "parameters": {
            "type": "object",
            "properties": {
                "setup": { "type": "string", "description": "The setup for the joke"},
                "punchline": {
                    "type": "string",
                    "description": "The punchline for the joke",
                },
                
            },
            "required": ["setup", "punchline"],
        }
    }
]



chain = (
    {"foo": RunnablePassthrough()}
    | prompt
    | model.bind(function_call={"name": "joke"}, functions=functions)
    | JsonKeyOutputFunctionsParser(key_name="setup")
)

joke = chain.invoke("Ducks")
pprint(joke)

