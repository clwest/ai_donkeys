from operator import itemgetter
import os
from dotenv import load_dotenv
from pprint import pprint

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful chatbot"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ]
)

memory = ConversationBufferMemory(return_messages=True)

chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | model
)

inputs = {"input": "Hi I'm Todd"}
response = chain.invoke(inputs)
# pprint(response)

memory.save_context(inputs, {"output": response.content})
memory.load_memory_variables({})

inputs = {"input": "What's my name?"}
response = chain.invoke(inputs)
pprint(response)
