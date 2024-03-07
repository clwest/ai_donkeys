import logging
import os
from pprint import pprint
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone

# Set logging for the queries
import logging
from factory.pinecone_factory import init_pinecone

load_dotenv()
init_pinecone()
index = "donkey-betz"
openai_api = os.getenv("OPENAI_API")


# Set up logging to see your queries
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

prompt_template = """You are an AI language model assistant.

Your task is to generate 3 different versions of the given user question to retrieve relevant documents from a vector database.

By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations  of distance-based similarity search.

Provide these alternative questions separated by newlines.

Original question: {question}"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["question"])


def multi_query_retriever(query):
    logging.info("Initializing embeddings and Pinecone document search")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", openai_api_key=openai_api
    )

    logging.info("Loading embeddings into retrievers")
    retriever = Pinecone.from_existing_index(
        embedding=embeddings,
        index_name=index,
    )

    logging.info("Setting up ChatOpenAI model")
    llm = ChatOpenAI(
        verbose=True,
        model="gpt-3.5-turbo",
        temperature=0.3,
        openai_api_key=openai_api,
    )
    logging.info(f"Initializing conversation summary memory for: {llm}")

    multi_query = MultiQueryRetriever.from_llm(
        retriever=retriever.as_retriever(), llm=llm, prompt=PROMPT
    )

    unique_docs = multi_query.get_relevant_documents(query)

    pprint(f"The following unique documents: {unique_docs}")
    return unique_docs


if __name__ == "__main__":
    # response = multi_query_retriever("On the Stacks network, what is Gaia?")
    # pprint(response)
    multi_query_retriever()
