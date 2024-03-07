# utils.py

import spacy
import requests
from retrying import retry

from metadata.transformers import *
from services.logging_config import root_logger as logger

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")


class Document:
    def __init__(self, content, metadata=None, lemmatized_text=None):
        self.content = content
        self.metadata = metadata or {"title": ""}
        self.lemmatized_text = lemmatized_text or content

    @property
    def title(self):
        return self.metadata.get("title", "No Title")


@retry(stop_max_attempt_number=3, wait_fixed=3000)
def fetch_url(url):
    """Fetch content from a URL with retries"""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    return response.text


def process_generic(document, nlp, project_title, project_name):
    """Generalized processing function for all document types"""
    logger.info(f"Document type: {type(document)}, attributes: {dir(document)}")
    cleaned_text = clean_text(document.content)
    lemmatized_text = lemmatize_text(cleaned_text, nlp)
    title = document.metadata.get("title", f"{project_title}, {project_name}")
    metadata_dict = {"title": title, "project": project_name}

    return Document(content=lemmatized_text, metadata=metadata_dict)
