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

# import git
from git import Repo
from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

load_dotenv()

openai_key = os.getenv("OPENAI_API")
nlp = spacy.load("en_core_web_sm")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# Clone
repo_path = "/repos"
repo = Repo.clone_from("https://github.com/langchain-ai/langchain", to_path=repo_path)

loader = GenericLoader.from_filesystem(
    repo_path + "/libs/langchain/langchain",
    glob="**/*",
    suffixes=[".py"],
    exclude=["**/non-utf8-encoding.py"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
)
documents = loader.load()
len(documents)
