import torch
import torch.nn as nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from src.utils import get_device


class MeanMaxPooling(nn.Module):
    """
    (C, B, E) -> (B, 2*E)
    where C is context count, B is batch size and E is embedding size.
    """

    def __init__(self, axis=0, dropout=0.0):
        super(MeanMaxPooling, self).__init__()
        self.axis = axis
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, inputs, valid_length=None):
        mean_out = torch.mean(inputs, dim=self.axis) if valid_length is None \
            else torch.sum(inputs, dim=self.axis) / valid_length
        max_out = torch.max(inputs, dim=self.axis).values
        outputs = torch.cat((mean_out, max_out), dim=1)
        outputs = self.dropout(outputs)
        return outputs


class ContextTransformer(nn.Module):
    """
    Transform context value to encoded embeddings
    [(B, 1) * C] -> (B, cross_size)
    """

    def __init__(
            self,
            context_dims,
            context_embed_size,
            context_num_heads,
            context_hidden_size,
            context_transformer_dropout,
            context_num_layers,
            context_pooling_dropout,
            cross_size,
            device,
    ):
        super(ContextTransformer, self).__init__()
        self.context_embedding = [nn.Embedding(context_dim, context_embed_size).to(device)
                                  for context_dim in context_dims]
        encoder_layers = TransformerEncoderLayer(d_model=context_embed_size,
                                                 nhead=context_num_heads,
                                                 dropout=context_transformer_dropout,
                                                 dim_feedforward=context_hidden_size,
                                                 activation='relu').to(device)
        self.context_encoder = TransformerEncoder(encoder_layers, num_layers=context_num_layers).to(device)
        self.context_pooling_dp = MeanMaxPooling(dropout=context_pooling_dropout)
        self.context_dense = torch.nn.Linear(in_features=2 * context_embed_size, out_features=cross_size).to(device)

    def forward(self, input_context_list):
        """
        context_input should be a list of tensors like [(B, 1) * S]
        """
        # [(B, 1) * C]
        context_embedding_list = [self.context_embedding[i](input_context)
                                  for i, input_context in enumerate(input_context_list)]  # -> [(B, 1, E) * C]
        context_out = torch.cat(context_embedding_list, dim=1).transpose(0, 1)  # -> (B, C, E) -> (C, B, E)

        context_out = self.context_encoder(context_out)  # -> (C, B, E)
        context_out = self.context_pooling_dp(context_out)  # -> (B, 2*E)
        context_out = self.context_dense(context_out)  # -> (B, cross_size)
        # print(context_out.shape)
        return context_out


class SequenceTransformer(nn.Module):
    """
    (B, 5) -> (B, cross_size)
    """

    def __init__(
            self,
            item_dim,
            item_embed_size,
            item_max_length,
            item_num_heads,
            item_hidden_size,
            item_transformer_dropout,
            item_num_layers,
            item_pooling_dropout,
            item_embedding_weight,
            cross_size,
            device,
    ):
        super(SequenceTransformer, self).__init__()
        if item_embedding_weight is not None:
            self.item_embedding = nn.Embedding.from_pretrained(item_embedding_weight, freeze=True).to(device)
        else:
            self.item_embedding = nn.Embedding(item_dim, item_embed_size).to(device)
        encoder_layers = TransformerEncoderLayer(d_model=item_embed_size,
                                                 nhead=item_num_heads,
                                                 dropout=item_transformer_dropout,
                                                 dim_feedforward=item_hidden_size,
                                                 activation='relu').to(device)
        self.item_encoder = TransformerEncoder(encoder_layers, num_layers=item_num_layers).to(device)
        self.item_pooling_dp = MeanMaxPooling(dropout=item_pooling_dropout)
        self.item_dense = torch.nn.Linear(in_features=2 * item_embed_size, out_features=cross_size).to(device)

    def forward(self, input_item_seq):
        # print("initial_shape:",input_item.shape)
        # (B, 5)
        item_embed_out = self.item_embedding(input_item_seq.long())  # -> (B, 5, E)
        item_embed_out = item_embed_out.transpose(0, 1)  # -> (B, 5, E) -> (5, B, E)
        item_out = self.item_encoder(item_embed_out)
        item_out = self.item_pooling_dp(item_out)  # -> (B, 2*E)
        item_out = self.item_dense(item_out)  # -> (B, cross_size)

        return item_out


class TxTFeaturesExtractor(nn.Module):
    """

    """

    def __init__(
            self,
            item_dim,
            context_dims,
            act_type="gelu",
            cross_size=100,
            context_embed_size=100,
            context_num_heads=2,
            context_hidden_size=512,
            context_transformer_dropout=0.0,
            context_num_layers=2,
            context_pooling_dropout=0.0,
            item_max_length=8,  # TODO: not using now
            item_embed_size=100,
            item_num_heads=4,
            item_hidden_size=256,
            item_transformer_dropout=0.0,
            item_num_layers=2,
            item_pooling_dropout=0.1,
            item_embedding_weight=None,
            device="auto",
    ):
        super(TxTFeaturesExtractor, self).__init__()
        device = get_device(device)
        self.features_dim = cross_size
        self.context_transformer = ContextTransformer(
            context_dims=context_dims,
            context_embed_size=context_embed_size,
            context_num_heads=context_num_heads,
            context_hidden_size=context_hidden_size,
            context_transformer_dropout=context_transformer_dropout,
            context_num_layers=context_num_layers,
            context_pooling_dropout=context_pooling_dropout,
            cross_size=cross_size,
            device=device,
        )
        self.sequence_transformer = SequenceTransformer(
            item_dim=item_dim,
            item_embed_size=item_embed_size,
            item_max_length=item_max_length,
            item_num_heads=item_num_heads,
            item_hidden_size=item_hidden_size,
            item_transformer_dropout=item_transformer_dropout,
            item_num_layers=item_num_layers,
            item_pooling_dropout=item_pooling_dropout,
            item_embedding_weight=item_embedding_weight,
            cross_size=cross_size,
            device=device,
        )
        self.dense1 = nn.Linear(cross_size, item_dim // 2).to(device)
        if act_type == "relu":
            self.act = nn.ReLU()
        elif act_type == "gelu":
            self.act = nn.GELU()
        elif act_type == "leakyRelu":
            self.act = nn.LeakyReLU(0.2)
        else:
            raise NotImplementedError
        self.dense2 = nn.Linear(item_dim // 2, item_dim).to(device)

    def forward(self, input_context_list, input_item_seq):
        # input [(B, 1) * C] and (B, 5)
        context_outs = self.context_transformer(input_context_list)  # -> (B, cross_size)
        item_outs = self.sequence_transformer(input_item_seq)  # -> (B.cross_size)
        outs = torch.mul(item_outs, context_outs)  # -> (B, cross_size)
        outs = self.dense1(outs)  # -> (B, item_dim//2)
        outs = self.act(outs)
        outs = self.dense2(outs)  # -> (B, item_dim)
        return outs
