"""
Basic configuration parameters:
"""
import torch


class GPTConfig:
    # Model parameters
    num_layers = 12  # Number of transformer layers
    d_model = 768  # Embedding dimension
    num_heads = 12  # Number of attention heads
    vocab_size = 50257  # Size of Vocabulary
    max_length = 1024  # Maximum sequence length

    # Training parameters
    batch_size = 32
    learning_rate = 3e-4
    epochs = 50

    # Other parameters
    device = (
        "cuda" if torch.cuda.is_available() else "cpu"
    )  # Training on GPU if available
