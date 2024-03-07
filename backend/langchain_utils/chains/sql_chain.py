import os
import logging
from dotenv import load_dotenv

from langchain.chains import LLMMathChain
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
connection = os.getenv("DEV_DATABASE_URL")

sql_chain = SQLDatabaseChain(connection)

# results = sql_chain.query("SELECT ")

print(sql_chain)