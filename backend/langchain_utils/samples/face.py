import logging
import os
from pprint import pprint
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from datasets import load_dataset
from langchain.evaluation.qa import QAEvalChain
from factory.pinecone_factory import init_pinecone

load_dotenv()
init_pinecone()
index_name = os.getenv("PINECONE_INDEX")
logging.info(f"Pinecone index name: {index_name}")
openai_api = os.getenv("OPENAI_API")

# prompt = PromptTemplate(
#     template="Question: {question}\nAnswer:", input_variables=["question"]
# )

prompt = PromptTemplate(
    template="Instruction: {instruction}\nResponse:", input_variables=["instruction"]
)

llm = OpenAI(
    verbose=True,
    openai_api_key=openai_api,
)
chain = LLMChain(llm=llm, prompt=prompt)

# This one works
# dataset = load_dataset("truthful_qa", "generation")
dataset = load_dataset("Omnibus/blockchain-tree")
print(dataset)
# dataset = load_dataset("fka/awesome-chatgpt-prompts")
# dataset = load_dataset("ise-uiuc/Magicoder-Evol-Instruct-110K")
# examples = list(dataset["validation"])[:5]
examples = list(dataset["train"])[:5]

predictions = chain.apply(examples)
print(predictions)

llm = OpenAI(
    temperature=0,
    openai_api_key=openai_api,
)

# graded_outputs = eval_chain.evaluate(
#     examples,
#     predictions,
#     instruction="question",
#     response="best_answer",
#     prediction_key="text",
# )

# Format examples for the chain
formatted_examples = [{"instruction": example["instruction"]} for example in examples]

# Apply the chain to the examples
predictions = chain.apply(formatted_examples)
eval_chain = QAEvalChain.from_llm(llm)

# Prepare data for evaluation
eval_data = [
    {
        "question": example["instruction"],
        "answer": example["response"],
        "prediction": prediction["text"],
    }
    for example, prediction in zip(examples, predictions)
]

# Evaluate the predictions
graded_outputs = eval_chain.evaluate(
    examples=eval_data,
    question_key="question",
    answer_key="answer",
    predictions="prediction",
)

# Print the predictions
for example, prediction in zip(examples, predictions):
    pprint(f"Instruction: {example['instruction']}")
    pprint(f"Response: {example['response']}")
    pprint(f"Model Prediction: {prediction['text']}\n")
