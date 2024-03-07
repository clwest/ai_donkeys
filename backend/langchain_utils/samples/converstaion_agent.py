from operator import itemgetter
import logging
import os
from pprint import pprint
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, load_tools
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts.chat import ChatPromptValue
from langchain.tools import WikipediaQueryRun
from langchain.tools.render import format_tool_to_openai_function
from langchain.utilities import WikipediaAPIWrapper
from langchain.chains import LLMCheckerChain

from langchain_utils.prompts.initial_prompts import starting_template

load_dotenv()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")


wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=10_000)
)
tools = [wiki]


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", starting_template),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm = OpenAI(
    temperature=0.3,
    openai_api_key=openai_api,
)

chat = ChatOpenAI(
    verbose=True,
    model="gpt-3.5-turbo",
    temperature=0.3,
    openai_api_key=openai_api,
)


def condense_prompt(prompt: ChatPromptValue) -> ChatPromptValue:
    messages = prompt.to_messages()
    num_tokens = chat.get_num_tokens_from_messages(messages)
    ai_function_messages = messages[2:]
    while num_tokens > 4_000:
        ai_function_messages = ai_function_messages[2:]
        num_tokens = chat.get_num_tokens_from_messages(
            messages[:2] + ai_function_messages
        )
    messages = messages[:2] + ai_function_messages
    return ChatPromptValue(messages=messages)


agent = (
    {
        "input": itemgetter("input"),
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | chat.bind(functions=[format_tool_to_openai_function(t) for t in tools])
    | OpenAIFunctionsAgentOutputParser()
)

fact_check = LLMCheckerChain.from_llm(llm, verbose=True)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
text = agent_executor.invoke(
    {
        "input": "Is there staking available on the Stacks network?  If so how does it work and what is your source of data for the answer?"
    }
)
pprint(text)
# fact_check.run(text)
