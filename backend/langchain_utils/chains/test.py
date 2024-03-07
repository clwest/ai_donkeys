import logging
import os
from pprint import pprint
from dotenv import load_dotenv

# from langchain.tools.vectorstore.tool import VectorStoreQATool
# from langchain.agents import AgentExecutor, AgentType, initialize_agent
# from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.schema.runnable import RunnableMap
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser


from factory.pinecone_factory import init_pinecone


load_dotenv()
init_pinecone()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api)
vectorstore = Pinecone.from_existing_index(embedding=embeddings, index_name=index_name)

retriever = vectorstore.as_retriever()

model = ChatOpenAI(
    verbose=True,
    model="gpt-3.5-turbo",
    temperature=0.3,
    openai_api_key=openai_api,
)

output_parser = StrOutputParser()

# chain = prompt | model | output_parser

template = """Answer the question based only on the following context:
           {context}

           Question: {question}
           """


prompt = ChatPromptTemplate.from_template(template)

chain = (
    RunnableMap(
        {
            "context": lambda x: retriever.get_relevant_documents(x["question"]),
            "question": lambda x: x["question"],
        }
    )
    | prompt
    | model
    | output_parser
)

test = chain.invoke({"question": "What is the Stacks Blockchain?"})

pprint(test)

inputs = (
    RunnableMap(
        {
            "context": lambda x: retriever.get_relevant_documents(x["question"]),
            "question": lambda x: x["question"],
        }
    )
    | prompt
    | model
    | output_parser
)

input = inputs.invoke({"question": "What is the Stacks Blockchain"})
pprint(input)
