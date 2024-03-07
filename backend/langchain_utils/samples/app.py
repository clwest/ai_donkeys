import os
from dotenv import load_dotenv
from pprint import pprint

# import spacy
from services.logging_config import root_logger as logger
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.vectorstores.pgvector import PGVector
from langchain_openai import OpenAIEmbeddings
from typing import Dict

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# nlp = spacy.load("en_core_web_sm")


# Basic Chatbot
# Conversation, Task Manager, Assistant
chat = ChatOpenAI(
    model="gpt-4-0125-preview", temperature=0.2
)

demo_chat_history = ChatMessageHistory()

demo_chat_history.add_user_message("Hey there! I'm Nemo the Fish")
demo_chat_history.add_ai_message("Hello!")
demo_chat_history.add_user_message("How are you today?")
demo_chat_history.add_ai_message("Fine thank you!")
demo_chat_history.messages

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability. The provided chat history includes facts about the user you are speaking with.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chain = prompt | chat


chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: demo_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

"""
Creates a function that will distill previous interactions into a summary. This can be added to the front of the chain too.
"""


def summarize_messages(chain_input):
    stored_messages = demo_chat_history.messages
    if len(stored_messages) == 0:
        return False
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "user",
                "Distill the above chat messages into a single summary message. Include as many specific details as you can.",
            ),
        ]
    )
    summarization_chain = summarization_prompt | chat

    summary_message = summarization_chain.invoke({"chat_history": stored_messages})

    demo_chat_history.clear()

    demo_chat_history.add_message(summary_message)

    return True


chain_with_summarization = (
    RunnablePassthrough.assign(messages_summarized=summarize_messages)
    | chain_with_message_history
)

name = chain_with_summarization.invoke(
    {"input": "What did I say my name was?"}, {"configurable": {"session_id": "unused"}}
)

# convo = demo_chat_history.messages
# print(convo)

# from langchain_utils.loaders.process_urls import ingest_urls

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
data = loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)


embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=embeddings)

retriever = vectorstore.as_retriever(k=4)

docs = retriever.invoke("Can LangSmith help test my LLM applications?")


SYSTEM_TEMPLATE = """
Answer the user's questions based on the below context.
If the context doesn't contain any relevant information to the question, don't make something up and just say "I don't know":

<context>
{context}
</context>
"""

question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_TEMPLATE,
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

document_chain.invoke(
    {
        "context": docs,
        "messages": [
            HumanMessage(content="Can LangSmith help test my LLM applications?")
        ],
    }
)


def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


retrieval_chain = RunnablePassthrough.assign(
    context=parse_retriever_input | retriever,
).assign(answer=document_chain)

resp = retrieval_chain.invoke(
    {"messages": [HumanMessage(content="Can Langchain help test my LLM applications?")]}
)
# pprint(resp)


info = retriever.invoke("Tell me more!")
# pprint(info)


query_transform_prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation. Only respond with the query, nothing else.",
        ),
    ]
)

query_transformation_chain = query_transform_prompt | chat

test = query_transformation_chain.invoke(
    {
        "messages": [
            HumanMessage(content="Can LangSmith help test my LLM applications?"),
            AIMessage(
                content="Yes, LangSmith can help test and evaluate your LLM applications. It allows you to quickly edit examples and add them to datasets to expand the surface area of your evaluation sets or to fine-tune a model for improved quality or reduced costs. Additionally, LangSmith can be used to monitor your application, log all traces, visualize latency and token usage statistics, and troubleshoot specific issues as they arise."
            ),
            HumanMessage(content="Tell me more!"),
        ],
    }
)

pprint(test)

"""
Trim the conversation to only contain the last two input/outputs
"""
def trim_messages(chain_input):
    stored_messages = demo_chat_history.messages
    if len(stored_messages) <= 2:
        return False

    demo_chat_history.clear()

    for message in stored_messages[-2:]:
        demo_chat_history.add_message(message)
    return True


chain_with_trimming = (
    RunnablePassthrough.assign(messages_trimmed=trim_messages)
    | chain_with_message_history
)

message = chain_with_trimming.invoke(
    {"input": "Where does P. Sherman live?"}, {"configurable": {"session_id": "unused"}}
)
# print(message)
