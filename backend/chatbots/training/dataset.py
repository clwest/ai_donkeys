"""
Loading and preprocessing PDFs, URLs, YouTube videos as datasets for training.
"""

import torch
from torch.utils.data import Dataset


class GPTDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.inputs = [self.tokenizer.encode(text)[:max_length] for text in texts]

    def preprocess(self):
        return len(self.inputs)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        input_ids = self.inputs[idx]
        # Creating input and target sequences for GPT
        input_ids = input_ids + [0] * (self.max_length - len(input_ids))  # Padding
        return torch.tensor(input_ids, dtype=torch.long)
