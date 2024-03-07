import os
import shutil
import tempfile
import requests
import spacy
import git
from pprint import pprint
from dotenv import load_dotenv
from langchain_community.document_loaders import GitLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.logging_config import root_logger as logger
from metadata.extractors import *
from metadata.transformers import *

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
nlp = spacy.load("en_core_web_sm")
branches = ["master", "main", "develop"]


class Document:
    def __init__(self, content, metadata=None, lemmatized_text=None):
        self.page_content = content
        self.metadata = metadata or {"title": ""}
        self.lemmatized_text = lemmatized_text or content

    @property
    def title(self):
        return self.metadata.get("title", "No Title")


def ingest_repos(batch_repos, repo_title, project_name):
    processed_repos = []

    for repo_url in batch_repos:
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Cloning repo: {repo_url} into {temp_dir}")

        try:
            git_repo = git.Repo.clone_from(repo_url, temp_dir)
        except git.GitCommandError as e:
            logger.error(f"Failed to clone repo: {repo_url}. Error: {e}")
            continue

        branches_to_try = ["master", "main"]
        for branch in branches_to_try:
            if branch in git_repo.heads:
                try:
                    loader = GitLoader(
                        clone_url=repo_url,
                        repo_path=temp_dir,
                        branch=branch,
                    )
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000, chunk_overlap=200
                    )
                    repo_list = loader.load_and_split(text_splitter)

                    for repo in repo_list:
                        processed_repo = process_urls(
                            repo, nlp, repo.metadata, repo_title, project_name
                        )
                        processed_repos.append(processed_repo)

                except requests.RequestException as e:
                    pprint(f"Failed to fetch repo from URL: {repo_url}. Error: {e}")
                    logger.error(
                        f"Failed to fetch GitHub Repo from Git Clone: {repo_url}. Error: {e}"
                    )
        shutil.rmtree(temp_dir)
    return processed_repos


def process_urls(doc, nlp, metadata, repo_title, project_name):
    """Process individual document for metadata, content, and embeddings"""
    # Process each document and add to processed_docs
    cleaned_text = clean_text(doc.page_content)
    lemmatized_text = lemmatize_text(cleaned_text, nlp)
    title = metadata.get("title", "No Title")
    if title == "No Title":
        title = f"{repo_title} Repo"
    metadata_dict = {
        "title": repo_title,
        "project": project_name,
        "source_type": "github",
    }

    logger.debug(
        f"Processed URL '{title}' with content length: {len(lemmatized_text)} characters"
    )

    processed_data = Document(content=lemmatized_text, metadata=metadata_dict)
    return processed_data


if __name__ == "__main__":
    ingest_repos()
