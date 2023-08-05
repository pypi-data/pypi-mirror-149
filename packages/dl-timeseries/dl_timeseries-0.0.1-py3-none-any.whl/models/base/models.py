import torch
import torch.nn as nn, Tensor
import torch.nn.functional as F



class EmbeddingNetwork(nn.Module):
    def __init__(
        self, 
        units, 
        no_embedding, 
        emb_dim
    ):
        super(EmbeddingNetwork, self).__init__()
        self.units=units
        self.no_embedding = no_embedding
        self.emb_dim = emb_dim
        self.embedding = nn.Embedding(self.no_embedding, self.emb_dim)
        self.linear = nn.Linear(self.emb_dim, self.units)
        self.out = nn.Linear(self.units, 1)
        
    def forward(self, x):
        x = F.relu(self.embedding(x))
        x = F.relu(self.linear(x))
        x = self.out(x)
        return x


class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        """
        Args:
            x: Tensor, shape [seq_len, batch_size, embedding_dim]
        """
        x = x + self.pe[ :x.size(0)]
        return self.dropout(x)


class NeuralNetwork(nn.Module):
    
    def __init__(
        self, 
        in_features, 
        out_features, 
        units=512, 
        no_embedding=None, 
        emb_dim=None):

        super(NeuralNetwork, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.units = units
        self.no_embedding = no_embedding
        self.emb_dim = emb_dim
        self.flatten = nn.Flatten()
        if no_embedding and emb_dim:
            self.embedding = nn.Embedding(self.no_embedding, self.emb_dim)
            self.emb_input = nn.Linear(self.emb_dim, self.units)
            self.emb_output = nn.Linear(self.units, self.out_features)
        
        self.cont_input = nn.Linear(self.in_features, self.units)
        self.hidden_layer = nn.Linear(8, 8)
        self.output_layer = nn.Linear(8, self.out_features)

    def forward(self, x, x_cat=None):
        """Add categorical data"""
        if x_cat is not None:
            x_out = self.embedding(x_cat)#.view((x_cat.shape[0], -1))
            x_out = F.relu(self.emb_input(x_out))
            x_out = self.emb_output(x_out)#.view(x_cat.shape[0], -1)

        x = F.relu(self.cont_input(x))
        x = torch.cat((x, x_out.view((x_cat.shape[0], -1))), dim=1)
        x = F.relu(self.hidden_layer(x))
        x = self.output_layer(x)
        return x
    