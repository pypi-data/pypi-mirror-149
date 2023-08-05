import torch
from torch import nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer
from .txt import MeanMaxPooling, PositionalEncoding, ContextTransformer, SequenceTransformerHistory
from .mmoe import MMoE


# Transformer x Embedding x Embedding as Bottom

class SequenceTransformerHistoryLite(SequenceTransformerHistory):
    def __init__(self, seq_num, cross_size, seq_embed_size=200, seq_max_length=8, seq_num_heads=4,
                 seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                 seq_pe=True):
        super(SequenceTransformerHistory, self).__init__()
        self.seq_embedding = nn.Embedding(seq_num, seq_embed_size)
        self.seq_pos = seq_pe
        self.seq_embed_size = seq_embed_size
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_size,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_size,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.seq_dense = torch.nn.Linear(in_features=2 * seq_embed_size, out_features=cross_size)


class ContextEmbedding(nn.Module):
    """
    [[B, ] * C] -> [B, cross_size]
    """
    def __init__(self, ctx_nums, cross_size, ctx_embed_size=100, ctx_num_heads=2,
                 ctx_hidden_size=512, ctx_num_layers=1, ctx_transformer_dropout=0.0,
                 ctx_pooling_dropout=0.0, ctx_pe=False):
        super().__init__()
        if isinstance(ctx_embed_size, int):
            self.ctx_embedding = nn.ModuleList([
                nn.Embedding(ctx_num, ctx_embed_size)
                for ctx_num in ctx_nums
            ])
            dense_in = len(ctx_nums) * ctx_embed_size
        elif isinstance(ctx_embed_size, list) or isinstance(ctx_embed_size, tuple):
            self.ctx_embedding = nn.ModuleList([
                nn.Embedding(ctx_num, ctx_embed)
                for ctx_num, ctx_embed in zip(ctx_nums, ctx_embed_size)
            ])
            dense_in = sum(ctx_embed_size)
        else:
            raise NotImplementedError()
        self.ctx_pe = False
        self.ctx_embed_size = ctx_embed_size
        self.ctx_dense = torch.nn.Linear(in_features=dense_in, out_features=cross_size)

    def forward(self, ctx_in):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :return: Tensor, shape [batch_size, cross_size]
        """
        # [[B, ] * C]
        ctx_embedding_list = [self.ctx_embedding[i](input_ctx).unsqueeze(1)
                              for i, input_ctx in enumerate(ctx_in)]  # -> [(B, 1, E_i) * C]
        ctx_out = torch.cat(ctx_embedding_list, dim=2).squeeze(1)  # -> [B, sum(E_i)]
        ctx_out = self.ctx_dense(ctx_out)  # -> (B, cross_size)
        return ctx_out


class TxEBottom(nn.Module):
    def __init__(self, ctx_nums, seq_num, ctx_cross_size=100, seq_cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_transformer_kwargs = context_transformer_kwargs if context_transformer_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.is_candidate_mode = is_candidate_mode
        self.features_dim = seq_cross_size + ctx_cross_size
        self.context_transformer = ContextEmbedding(
            ctx_nums=ctx_nums,
            cross_size=seq_cross_size,
            **context_transformer_kwargs,
        )
        self.sequence_transformer = SequenceTransformerHistoryLite(
            seq_num=seq_num,
            cross_size=ctx_cross_size,
            **sequence_transformer_kwargs,
        )
        if is_candidate_mode:
            # self.candidate_dense = nn.Linear(
            #     in_features=self.sequence_transformer.seq_embed_size,
            #     out_features=cross_size
            # )
            pass

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param candidate_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """
        # input [[B, 1] * C] and [B, 5]
        ctx_out = self.context_transformer(ctx_in=ctx_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        outs = torch.cat([seq_out, ctx_out], dim=1)  # -> [B, CROSS_seq + CROSS_ctx]
        if self.is_candidate_mode:
            candidate_embed = self.sequence_transformer.seq_embedding(candidate_in)
            outs = torch.concat([outs, candidate_embed], dim=1)  # -> [B, CROSS_seq + CROSS_ctx + seq_embed_size]
        return outs


class MultiTaskTxE(nn.Module):
    def __init__(self, ctx_nums, seq_num, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations,
                 ctx_cross_size=100, seq_cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        self.is_candidate_mode = is_candidate_mode
        self.shared_bottom = TxEBottom(
            ctx_nums=ctx_nums,
            seq_num=seq_num,
            ctx_cross_size=ctx_cross_size,
            seq_cross_size=seq_cross_size,
            is_candidate_mode=is_candidate_mode,
            context_transformer_kwargs=context_transformer_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        mmoe_input_size = ctx_cross_size + seq_cross_size + self.shared_bottom.sequence_transformer.seq_embed_size
        self.mmoe = MMoE(
            input_size=mmoe_input_size,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        bottom_features = self.shared_bottom(ctx_in, seq_in, vl_in, candidate_in, seq_history)
        outs = self.mmoe(bottom_features)
        return outs


# Transformer x Embedding x Embedding as Bottom

class TxTBottom(nn.Module):
    def __init__(self, ctx_nums, seq_num, cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_transformer_kwargs = context_transformer_kwargs if context_transformer_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.is_candidate_mode = is_candidate_mode
        self.features_dim = cross_size
        self.context_transformer = ContextTransformer(
            ctx_nums=ctx_nums,
            cross_size=cross_size,
            **context_transformer_kwargs,
        )
        self.sequence_transformer = SequenceTransformerHistory(
            seq_num=seq_num,
            cross_size=cross_size,
            **sequence_transformer_kwargs,
        )
        if is_candidate_mode:
            # self.candidate_dense = nn.Linear(
            #     in_features=self.sequence_transformer.seq_embed_size,
            #     out_features=cross_size
            # )
            pass

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param candidate_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """
        # input [[B, 1] * C] and [B, 5]
        ctx_out = self.context_transformer(ctx_in=ctx_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        outs = torch.mul(seq_out, ctx_out)  # -> [B, cross_size]
        if self.is_candidate_mode:
            candidate_embed = self.sequence_transformer.seq_embedding(candidate_in)
            outs = torch.concat([outs, candidate_embed], dim=1)  # -> [B, seq_embed_size]
        return outs


class MultiTaskTxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations,
                 cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        self.is_candidate_mode = is_candidate_mode
        self.shared_bottom = TxTBottom(
            ctx_nums=ctx_nums,
            seq_num=seq_num,
            cross_size=cross_size,
            is_candidate_mode=is_candidate_mode,
            context_transformer_kwargs=context_transformer_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        mmoe_input_size = cross_size + self.shared_bottom.sequence_transformer.seq_embed_size
        self.mmoe = MMoE(
            input_size=mmoe_input_size,
            expert_num=expert_num,
            expert_hidden_sizes=expert_hidden_sizes,
            task_num=task_num,
            task_hidden_sizes=task_hidden_sizes,
            task_last_activations=task_last_activations,
        )

    def forward(self, ctx_in, seq_in, vl_in, candidate_in, seq_history=None):
        bottom_features = self.shared_bottom(ctx_in, seq_in, vl_in, candidate_in, seq_history)
        outs = self.mmoe(bottom_features)
        return outs
