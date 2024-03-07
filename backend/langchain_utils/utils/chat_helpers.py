import spacy
from pprint import pprint
from services.logging_config import root_logger as logger

nlp = spacy.load("en_core_web_sm")


def generate_topic_name(query, nlp=nlp):
    doc = nlp(query)

    # Find the first noun pharse
    for np in doc.noun_chunks:
        return np.text

    # If no noun phrase is found try to find named entity
    for ent in doc.ents:
        return ent.text

    return "General Inquiry"


def generate_description(response):
    return (
        response.split(".")[0] if isinstance(response, str) else "Default Description"
    )
