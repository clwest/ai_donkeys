"""
Main training loop, loss function, and optimizer
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from model import GPT
from config import GPTConfig

# Load and prepare data
dataset = ...  # Add dataset
dataloader = DataLoader(dataset, batch_size=GPTConfig.batch_size, shuffle=True)

model = GPT(GPTConfig()).to(GPTConfig.device)
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=GPTConfig.learning_rate)


# Training loop
for epoch in range(GPTConfig.epochs):
    model.train()
    for batch in dataloader:
        inputs, targets = batch  # Get input and target sequences from dataset

        # Forward pass
        outputs = model(inputs)
        loss = loss_function(outputs.view(-1, GPTConfig.vocab_size), targets.view(-1))

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch+1}/{GPTConfig.epochs}, Loss: {loss.item()}")

    # Save the model
    torch.save(model.state_dict(), f"gpt-model-epoch-{epoch-1}.pt")

print(f"Training completed")
