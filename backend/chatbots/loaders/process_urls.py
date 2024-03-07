import os
import requests


from pprint import pprint
from dotenv import load_dotenv
from bs4 import BeautifulSoup as Soup

from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from retrying import retry
import spacy
import warnings


from metadata.extractors import *
from metadata.transformers import *
from services.logging_config import root_logger as logger


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")

# Suppress only the specific warning from BeautifulSoup
warnings.filterwarnings("ignore", category=Warning)


@retry(stop_max_attempt_number=3, wait_fixed=3000)
def fetch_url(url):
    """Fetch content from a URL with retries"""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.text


class Document:
    def __init__(self, content, metadata=None, lemmatized_text=None):
        self.page_content = content
        self.metadata = metadata or {"title": ""}
        self.lemmatized_text = lemmatized_text or content

    @property
    def title(self):
        return self.metadata.get("title", "No Title")


def ingest_urls(batch_urls, url_title, project_name):
    """Process and ingest documents from URLs"""
    processed_documents = []
    for url in batch_urls:
        try:
            # Load and process documents from each URL
            loader = RecursiveUrlLoader(
                url=url,
                max_depth=3,
                timeout=60,
                extractor=lambda x: Soup(x, "html.parser").text,
            )

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            docs_list = loader.load_and_split(text_splitter)

            for doc in docs_list:
                processed_doc = process_urls(
                    doc, nlp, doc.metadata, url_title, project_name
                )
                processed_documents.append(processed_doc)

        except requests.RequestException as e:
            pprint(f"Failed to fetch URL {url}. Error: {e}")
            logger.error(f"Failed to fetch URL {url} after 3 attempts: {e}")

    return processed_documents


def process_urls(doc, nlp, metadata, url_title, project_name):
    """Process individual document for metadata, content, and embeddings"""
    # Process each document and add to processed_docs
    cleaned_text = clean_text(doc.page_content)
    lemmatized_text = lemmatize_text(cleaned_text, nlp)
    title = metadata.get("title", "No Title")
    if title == "No Title":
        title = f"{url_title} Web"
    metadata_dict = {
        "title": url_title,
        "project": project_name,
        "source_type": "url",
    }

    logger.info(
        f"Processed URL '{title}' with content length: {len(lemmatized_text)} characters"
    )

    processed_data = Document(content=lemmatized_text, metadata=metadata_dict)
    return processed_data


if __name__ == "__main__":
    ingest_urls()
