import logging
import os
from pprint import pprint
from dotenv import load_dotenv

from langchain.chains import HypotheticalDocumentEmbedder, LLMChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from factory.pinecone_factory import init_pinecone


load_dotenv()
init_pinecone()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")

base_embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002", openai_api_key=openai_api
)
llm = OpenAI(
    verbose=True,
    # model="gpt-3.5-turbo",
    # temperature=0.3,
    openai_api_key=openai_api,
)


# Load with `web_search` prompt
embeddings = HypotheticalDocumentEmbedder.from_llm(llm, base_embeddings, "web_search")
# Now we can use it as any embedding class!
result = embeddings.embed_query("Where is the Taj Mahal?")
pprint(result)

multi_llm = OpenAI(verbose=True, openai_api_key=openai_api, n=4, best_of=4)
embeddings = HypotheticalDocumentEmbedder.from_llm(
    multi_llm, base_embeddings, "web_search"
)
# Now we can use it as any embedding class!
result = embeddings.embed_query("What cryptographic are on the Stacks network?")
pprint("Here are the results: {result}")
