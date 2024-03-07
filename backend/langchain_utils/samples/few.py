import os
import logging
from pprint import pprint
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from factory.token_factory import TokenCounterFactory

# Load environment variables
load_dotenv()

openai_api = os.getenv("OPENAI_API")

chat = ChatOpenAI(temperature=0.8, openai_api_key=openai_api)


template = "You are a helpful assistant that is loving, adorable and annoying all at the same time."

system_message_prompt = SystemMessagePromptTemplate.from_template(template)

example_human = SystemMessagePromptTemplate.from_template(
    "Hi", additional_kwargs={"name": "donkey_king"}
)

example_ai = SystemMessagePromptTemplate.from_template(
    "How can I help you sir?", additional_kwargs={"name": "donkey_assistant"}
)

human_template = "{text}"

human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, example_human, example_ai, human_message_prompt]
)
chain = LLMChain(llm=chat, prompt=chat_prompt)
# get a chat completion from the formatted messages

token_counter_factory = TokenCounterFactory()
token_counter = token_counter_factory.create_token_counter(chain)
results = token_counter(
    "Write a short blog about writing smart contracts and creating dApps on the Stacks network, and the differences between Clarity and Solidity."
)
pprint(f"Tokens for results: {results}")
# pprint(
#     chain.run(

#     )
# )
