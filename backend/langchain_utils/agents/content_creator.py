import os
import logging
from dotenv import load_dotenv
from langchain.agents.tools import Tool
from langchain.chains import LLMMathChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.utilities import DuckDuckGoSearchAPIWrapper
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.tools import WikipediaQueryRun, ArxivQueryRun
from langchain.utilities import WikipediaAPIWrapper


# Load environment variables
load_dotenv()

openai_api = os.getenv("OPENAI_API")
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name Content Creator: {index_name}")


def generate_content(user_id, user_query, index_name):
    from langchain_utils.prompts.content_prompt import create_few_shot_prompt
    from langchain_utils.samples.prompt_utils import combine_prompt_sets
    from langchain_utils.samples.semantic_search import create_similarty_selector

    combined_prompts = combine_prompt_sets()
    logging.info(
        f"Combined prompts in Content Creator {combined_prompts}"
    )  # Stopping here I think

    # example_selector = create_similarty_selector(index_name, user_id, user_query)
    # logging.info(f"Example selector in Content Creator {example_selector}")

    few_shot_prompt = create_few_shot_prompt(combined_prompts, user_query)
    logging.info(f"Few shot prompts in Content Creator {few_shot_prompt}")

    content_response = content_create(user_query, few_shot_prompt)
    logging.info(f"Content response in Content Creator")
    return content_response


def content_create(query, few_shot_prompt):
    # Initialize the search tool and LLM
    arvix = ArxivQueryRun()
    search = DuckDuckGoSearchAPIWrapper()
    wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    llm = OpenAI(temperature=0.8, openai_api_key=openai_api)
    llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

    # Set up the tools
    tools = [
        Tool(
            name="Arvix",
            func=arvix.run,
            description="Useful for searching research papers on Arvix.",
        ),
        Tool(
            name="Search",
            func=search.run,
            description="Useful for searching the internet",
        ),
        Tool(
            name="Calculator",
            func=llm_math_chain.run,
            description="useful for when you need to answer questions about math",
        ),
        Tool(
            name="Wikipedia",
            func=wiki.run,
            description="Useful for general knowledge and information.",
        ),
    ]

    # Initialize the model, planner, and executor
    model = ChatOpenAI(temperature=0.8, openai_api_key=openai_api)
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)

    # Initialize the PlanAndExecute agent
    agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
    logging.info(f"Planner Agent in Content Creator {agent}")
    full_prompt = f"{few_shot_prompt}\n{query}"
    logging.info(f"Full prompt from Content Creator {full_prompt}")
    # Execute the agent with the provided query
    return agent.run(full_prompt)


if __name__ == "__main__":
    content_create()
