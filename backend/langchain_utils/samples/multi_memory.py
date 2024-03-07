import os
from dotenv import load_dotenv
from pprint import pprint

from langchain.chains import ConversationChain
from langchain.memory import (
    CombinedMemory,
    ConversationBufferMemory,
    ConversationSummaryMemory,
)
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

conv_memory = ConversationBufferMemory(
    memory_key="chat_history_lines", input_key="input"
)

summary_memory = ConversationSummaryMemory(llm=OpenAI(), input_key="input")
# Combined
memory = CombinedMemory(memories=[conv_memory, summary_memory])
_DEFAULT_TEMPLATE = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Summary of conversation:
{history}
Current conversation:
{chat_history_lines}
Human: {input}
AI:"""
PROMPT = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"],
    template=_DEFAULT_TEMPLATE,
)
llm = OpenAI(temperature=0, openai_api_key=openai_key)
conversation = ConversationChain(llm=llm, verbose=True, memory=memory, prompt=PROMPT)

text = conversation.run("Hi!")
print(text)

joke = conversation.run("Tell me a joke")

pprint(joke)

ice_cream = conversation.run("Tell me a joke about McDonalds Ice Cream Machines.")
pprint(ice_cream)