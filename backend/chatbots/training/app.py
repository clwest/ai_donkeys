from transformers import GPT2Tokenizer
from dataset import GPTDataset

# Assuming 'processed_texts' is a list of your preprocessed texts
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
max_length = 1024  # or any suitable length
dataset = GPTDataset(processed_texts, tokenizer, max_length)
