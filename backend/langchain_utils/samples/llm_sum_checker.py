from langchain.chains import LLMSummarizationCheckerChain
from langchain.llms import OpenAI
from pprint import pprint
import os
import logging
from services.logging_config import root_logger as logger
from dotenv import load_dotenv

load_dotenv()

openai_api = os.getenv("OPENAI_API")

llm = OpenAI(temperature=0, openai_api_key=openai_api)
checker_chain = LLMSummarizationCheckerChain.from_llm(llm, verbose=True, max_checks=2)
text = """
'Investing in recycled water is a wise choice.'
"""

logger.info(f"Running a fact check on: {checker_chain.run(text)}")
