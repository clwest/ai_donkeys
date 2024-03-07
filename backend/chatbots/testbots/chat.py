import os
from dotenv import load_dotenv
from pprint import pprint


from services.logging_config import root_logger as logger
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory import ConversationTokenBufferMemory
from langchain.memory import ConversationSummaryBufferMemory



load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# Basic Chatbot
# Conversation, Task Manager, Assistant
llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125", temperature=0.0,

)

# memory = ConversationBufferMemory()




# name = conversation.predict(input="Hi, my name is Donkey")
# math = conversation.predict(input="What is 1+1")
# reminder = conversation.predict(input="What is my name?")
# print(memory.load_memory_variables({}))

# add = memory.save_context({"input": "Hi"},
#                     {"output": "What's up"})
# add1 = memory.save_context({"input": "Not much, just hanging"},
#                     {"output": "Cool"})

# print(memory.buffer)
# print(memory.load_memory_variables({}))

"""
    Short term memory example
    By adding the K=1 to the ConversationBufferWindowMemory the chatbot will only remember the last input from the User
"""

# short_term = ConversationBufferWindowMemory(k=1)

# conversation = ConversationChain(
#     llm=llm,
#     memory=short_term,
#     verbose=True
# )

# name = conversation.predict(input="Hi, my name is Donkey")
# math = conversation.predict(input="What is 1+1")
# reminder = conversation.predict(input="What is my name?")
# print(reminder)

"""
Working with Token Limits 
"""

# memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=30)
# memory.save_context({"input": "AI is what?!"},
#                     {"output": "Amazing!"})
# memory.save_context({"input": "Backpropagation is what?"},
#                     {"output": "Beautiful!"})
# memory.save_context({"input": "Chatbots are what?"}, 
#                     {"output": "Charming!"})

# token = memory.load_memory_variables({})
# print(token)

"""
    Working with summary's of the conversation. Instead of limiting tokens or dropping inputs, the LLM will summarize the conversation as it goes along
    and use that as the memory.
"""

# create a long string
schedule = "There is a meeting at 8am with your product team. \
You will need your powerpoint presentation prepared. \
9am-12pm have time to work on your LangChain \
project which will go quickly because Langchain is such a powerful tool. \
At Noon, lunch at the italian resturant with a customer who is driving \
from over an hour away to meet you to understand the latest in AI. \
Be sure to bring your laptop to show the latest LLM demo."

memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
memory.save_context({"input": "Hello"}, {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})
memory.save_context({"input": "What is on the schedule today?"}, 
                    {"output": f"{schedule}"})

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

text = memory.load_memory_variables({})
# print(text)


demo = conversation.predict(input="What would be a good demo to show?")

var = memory.load_memory_variables({})
print(var)