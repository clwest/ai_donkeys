"""
Implement GPT model structure to use with Pytorch
"""
import torch
import torch.nn as nn


class GPT(nn.Model):
    def __init__(self, config):
        super(GPT, self).__init__()
        # Embeddings layer for input
        self.token_embeddings = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embeddings = nn.Embedding(config.max_length, config.d_model)

        # Transformer block with multi-head attention and feedforward layers
        self.transformer_blocks = nn.ModuleList(
            [TransformerBlock(config) for _ in range(config.num_layers)]
        )

        # produce the final output from the transformer blocks
        self.output_layer = nn.Linear(config.d_model, config.vocab_size)

    def forward(self, x):
        token_embeddings = self.token_embeddings(x)
        position_ids = torch.arange(0, x.size(1), device=x.device).unsqueeze(0)
        position_embeddings = self.position_embeddings(position_ids)

        x = token_embeddings + position_embeddings
        for block in self.transformer_blocks:
            x = block(x)

        logits = self.output_layer(x)
        return logits


# Splits the input in multiple heads for parallel attention computations
# Combines the results from all heads
class MultiHeadAttention(nn.Module):
    def __init__(self, config):
        super(MultiHeadAttention, self).__init__()
        self.num_heads = config.num_heads
        self.d_model = config.d_model

        assert (
            self.d_model % self.num_heads == 0
        ), "d_model must be divisible by num_heads"

        self.depth = self.d_model // self.num_heads

        self.wq = nn.Linear(self.d_model, self.d_model)
        self.wk = nn.Linear(self.d_model, self.d_model)
        self.wv = nn.Linear(self.d_model, self.d_model)

        self.dense = nn.Linear(self.d_model, self.d_model)

    # reshapes the inputs for parallel computation across specified number of heads
    def split_heads(self, x, batch_size):
        x = x.view(batch_size, -1, self.num_heads, self.depth)
        return x.permute(0, 2, 1, 3)

    # Applies linear transformations, splits into heads, computes
    # scaled dot-product attention and then combines the heads back together
    def forward(self, q, k, v):
        batch_size = q.size(0)

        q = self.split_heads(
            self.wq(
                q,
            ),
            batch_size,
        )
        k = self.split_heads(self.wk(k), batch_size)
        v = self.split_heads(self.wv(v), batch_size)

        # Scaled dot-product attention
        matmul_qk = torch.matmul(q, k.transpose(-2, -1))
        scale = torch.sqrt(torch.tensor(self.depth, dtype=torch.float32))
        scaled_attention_logits = matmul_qk / scale
        attention_weights = nn.functional.softmax(scaled_attention_logits, dim=-1)

        output = torch.matmul(attention_weights, v)
        output = output.permute(0, 2, 1, 3).contiguous()
        output = output.view(batch_size, -1, self.d_model)

        return self.dense(output)


class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        """
        d_model is the model's dimension, and d_ff is the dimension of the feed-forward network, typically much larger than d_model.
        The ReLU activation provides non-linearity, and the dropout helps prevent overfitting.
        """
        super(PositionwiseFeedForward, self).__init__()
        # Initialize two linear layers with a ReLU activation between them

        # First linear layer
        self.linear1 = nn.Linear(d_model, d_ff)

        # Second linear layer
        self.linear2 = nn.Linear(d_ff, d_model)

        # ReLU activation and dropout
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Apply the first linear layer
        x = self.relu(self.linear1(x))
        # Apply ReLU activation
        x = self.dropout(x)
        # Apply the second linear layer
        x = self.linear2(x)
        return x


class TransformerBlock(nn.Module):
    def __init__(self, config):
        super(TransformerBlock, self).__init__()
        self.attention = MultiHeadAttention(config)
        self.feed_forward = PositionwiseFeedForward(
            config.d_model, config.d_model * 4, dropout=config.dropout
        )
        self.layer_norm1 = nn.LayerNorm(config.d_model)
        self.layer_norm2 = nn.LayerNorm(config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        # Attention part
        attention_output = self.attention(x, x, x)  # Self=attention
        x = x + self.dropout(attention_output)
        x = self.layer_norm1(x)

        # Feed-forward part
        ff_output = self.feed_forward(x)
        x = x + self.dropout(ff_output)
        x = self.layer_norm2(x)

        return x
