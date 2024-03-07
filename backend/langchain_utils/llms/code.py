import logging
import os
from pprint import pprint
from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain.vectorstores import Pinecone
from langchain.tools.memorize.tool import Memorize
import pinecone
from pinecone import Index
from factory.pinecone_factory import init_pinecone
from debuggers.debug_pinecone import debug_pinecone_retrieval

load_dotenv()
init_pinecone()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")
import warnings

warnings.filterwarnings("ignore")
from git import Repo
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language

repo_path = (
    "/Volumes/Donkey Betz/Development/DonkeyBetz/backend/langchain_utils/langchain_repo"
)
repo = (
    Repo.clone_from("https://github.com/langchain-ai/langchain", to_path=repo_path),
)
loader = GenericLoader.from_filesystem(
    repo_path + "/libs/langchain/langchain",
    glob="**/*",
    suffixes=[".py"],
    parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
)
documents = loader.load()
lg_docs = len(documents)

pprint(f"Langchain docs: {lg_docs}")

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
)

texts = python_splitter.split_documents(documents)

py_docs = len(texts)
pprint(f"Python Docs: {py_docs}")

embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002", openai_api_key=openai_api, disallowed_special=()
)

vectorstore = Pinecone.from_documents(texts, embeddings, index_name=index_name)


retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 8},
    index_name=index_name,
)

llm = ChatOpenAI(
    model_name="gpt-4",
    openai_api_key=openai_api,
)

memory = ConversationSummaryMemory(
    llm=llm, memory_key="chat_history", return_messages=True
)

qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

questions = [
    "What is the class hierarchy?",
    "What classes are derived from the Chain class?",
    "What one improvement do you propose in code in relation to the class hierarchy for the Chain class?",
]

for question in questions:
    result = qa(question)
    pprint(f"-> **Question**: {question} \n")
    pprint(f"**Answer**: {result['answer']} \n")
