import torch
import torch.nn as nn
import yfinance as yf
from datagenerator import generate_data

class StockTransformer(nn.Module):
    def __init__(self, input_dim, embedding_dim, num_layers, hidden_dim, output_dim=1):  # Output_dim set to 1 by default
        super().__init__()
        # Embedding layer
        self.embedding = nn.Linear(input_dim, embedding_dim)

        # Transformer encoder
        self.transformer_encoder = nn.TransformerEncoder(nn.TransformerEncoderLayer(d_model=embedding_dim, nhead=8, dim_feedforward=hidden_dim), num_layers=num_layers)

        # Output layer (1 neuron for direction prediction)
        self.output = nn.Linear(embedding_dim, output_dim)

    def forward(self, x):
        # Embed input
        x = self.embedding(x)

        # Pass through transformer encoder
        x = self.transformer_encoder(x)

        # Output layer (no softmax needed for single output)
        x = self.output(x)

        return x

if __name__ == '__main__':
    ticker = "NVDA"
    ticker = yf.Ticker(ticker)
    data = ticker.history(period='3mo', interval='1d')

    # Data preparation
    data['MA'] = data['Close'].rolling(window=30).mean()
    data = data.tail(30)  # Grab the most recent 30 days
    input_data = data[['Close', 'Volume', 'MA']]  # Filter out other values
    input_tensor = torch.tensor(input_data.values, dtype=torch.float32)

    # Adapt target data based on your chosen approach (binary or regression):
    # ... (Prepare target data for prediction) ...

    # Model and output
    model = StockTransformer(input_dim=(30, 3), embedding_dim=128, num_layers=4, hidden_dim=256)
    output = model(input_tensor)

    # Print relevant information
    print(input_data)  # Print input data for reference
    print(f"Predicted direction:\n{output.squeeze().item()}")  # Print the single predicted value
