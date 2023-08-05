import torch
from torch import nn
from .multitask import TxTBottom


class WideModel(nn.Module):
    def __init__(self, c_embed_size, ctx_nums, c_feature_nums, n_feature_nums):
        super().__init__()
        self.c_embedding = nn.ModuleList([
            nn.Embedding(c, c_embed_size)
            for c in ctx_nums
        ])
        self.dense = torch.nn.Linear(in_features=c_embed_size * c_feature_nums + n_feature_nums,
                                     out_features=1)

    def forward(self, c_in, n_in):
        c_embedding_list = [self.c_embedding[i](c)
                            for i, c in enumerate(c_in)]  # -> [(B, 1, E) * C]
        c_out = torch.cat(c_embedding_list, dim=1)  # -> (B, E * C)
        n_in = torch.stack(n_in, dim=1)
        outs = torch.cat([c_out, n_in], dim=1)
        outs = self.dense(outs)
        return outs


class DeepModel(nn.Module):
    def __init__(self, ctx_nums, seq_num, cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        self.txt_bottom = TxTBottom(
            ctx_nums=ctx_nums,
            seq_num=seq_num,
            cross_size=cross_size,
            is_candidate_mode=is_candidate_mode,
            context_transformer_kwargs=context_transformer_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        dense_input_size = cross_size + self.txt_bottom.sequence_transformer.seq_embed_size
        self.dense_1 = torch.nn.Linear(in_features=dense_input_size, out_features=dense_input_size//2)
        self.dense_2 = torch.nn.Linear(in_features=dense_input_size//2, out_features=1)
        self.act = nn.GELU()

    def forward(self, *deep_in):
        outs = self.txt_bottom(*deep_in)
        outs = self.dense_1(outs)
        outs = self.act(outs)
        outs = self.dense_2(outs)
        return outs


class WideAndDeep(nn.Module):
    def __init__(self, ctx_nums, seq_num, c_embed_size, c_feature_nums, n_feature_nums,
                 cross_size=200, is_candidate_mode=True,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        self.wide = WideModel(c_embed_size, ctx_nums, c_feature_nums, n_feature_nums)
        self.deep = DeepModel(
            ctx_nums=ctx_nums,
            seq_num=seq_num,
            cross_size=cross_size,
            is_candidate_mode=is_candidate_mode,
            context_transformer_kwargs=context_transformer_kwargs,
            sequence_transformer_kwargs=sequence_transformer_kwargs,
        )
        self.pred_dense = torch.nn.Linear(in_features=2, out_features=1)

    def forward(self, wide_in, deep_in):
        wide_outs = self.wide(*wide_in)
        deep_outs = self.deep(*deep_in)
        outs = torch.concat([wide_outs, deep_outs], dim=1)
        outs = self.pred_dense(outs)
        outs = torch.sigmoid(outs)
        return outs
