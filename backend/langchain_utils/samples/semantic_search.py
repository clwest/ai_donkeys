import os
from dotenv import load_dotenv
import logging
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import traceback
from langchain_utils.samples.prompt_utils import combine_prompt_sets

from langchain_utils.prompts.initial_prompts import (
    blockchain_and_ai_template,
    stacks_template,
)

# from models.users import UserPrompt
import helpers.custom_exceptions as ce
from factory import create_app
from factory.pinecone_factory import init_pinecone


load_dotenv()
app = create_app()
init_pinecone()

openai_key = os.getenv("OPENAI_API")
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name Semantic Search: {index_name}")


def semantic_similarity_search(query_text, index_name):
    Embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", openai_api_key=openai_key
    )

    vectorstore = Pinecone.from_existing_index(index_name, Embeddings)

    if not isinstance(query_text, str) or not query_text.strip():
        logging.error(f"Invalid query text: {query_text}")
        return {}

    query_embeddings = Embeddings.embed_query(query_text)

    if not query_embeddings:
        logging.error(f"Failed to generate query embeddings or embeddings are empty ")
        return {}

    k = 5
    results = None
    try:
        embeddings_str = " ".join(map(str, query_embeddings))
        results = vectorstore.similarity_search(embeddings_str, k)
        logging.info(f"Results for semantic seach {results}")
    except Exception as e:
        logging.error(f"Error during similarity search {e}")
        logging.error(f"Traceback: ", exc_info=True)
    return results if results is not None else {}


def create_similarty_selector(index_name, user_id, *prompt_sets):
    combined_prompts = combine_prompt_sets(user_id, *prompt_sets)
    logging.info(f"Type of combined prompts: {type(combined_prompts)}")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002", openai_api_key=openai_key
    )

    VectorStore = Pinecone.from_existing_index("donkey-betz", embeddings)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        combined_prompts,
        embeddings,
        vectorstore_cls=VectorStore,
        k=2,
    )
    logging.info(f"Some examples from example selector: {example_selector}")
    # Add examples to the vectorstore and perform selection
    search_results = []
    for prompt in combined_prompts:
        logging.info(f"Proccessing prompt: {prompt}")
        selected_examples = example_selector.select_examples(prompt)
        for example in selected_examples:
            results = semantic_similarity_search(example["input"])
            if results:
                search_results.append(results)

    return search_results


if __name__ == "__main__":
    create_similarty_selector()
