from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    """TextCNN

    Args:
        embeddings_dim0 (int):
        embeddings_dim1 (int):
        embeddings_pretrained (Optional[torch.Tensor]):
        embeddings_pretrained_freeze (bool):
        conv_kernel_sizes (list[int]):
        outpu_dim (int):
    """

    def __init__(
        self,
        # embeddings
        embeddings_dim0: int,
        embeddings_dim1: int,  # D
        embeddings_pretrained: Optional[torch.Tensor] = None,
        embeddings_pretrained_freeze: bool = False,
        # convs
        conv_kernel_sizes: Optional[list[int]] = None,
        # output
        output_dim: int = 128,
    ) -> None:
        super(TextCNN, self).__init__()

        # embeddings
        self.embedding = nn.Embedding(
            num_embeddings=embeddings_dim0, embedding_dim=embeddings_dim1
        )
        if embeddings_pretrained is not None:
            self.embedding.from_pretrained(
                embeddings_pretrained, freeze=embeddings_pretrained_freeze
            )

        # convs
        if conv_kernel_sizes is None:
            conv_kernel_sizes = [1]

        self.convs = nn.ModuleList(
            [
                nn.Conv2d(
                    in_channels=1,
                    out_channels=output_dim,
                    kernel_size=(kernel_size, embeddings_dim1),
                )
                for kernel_size in conv_kernel_sizes
            ]
        )

    def forward(self, x_ids: torch.LongTensor) -> torch.Tensor:
        """
        - B: batch size
        - N: number of sequencies
        - L: number of tokens in each sequence

        x_ids == (B, L)
        x_embs = (B, D)

        x_ids == (N, B, L)
        x_embs = (N, B, D)

        Args:
            x_ids (torch.LongTensor):

        Returns:
            x_embs (torch.Tensor):
        """
        # x_ids.shape: (N, [B], L)
        # x_ids_reshaped.shape: (N, B[=1], L)
        match x_ids.dim():
            case 2:
                x_ids_unsqueezed = x_ids.unsqueeze(1)
            case 3:
                x_ids_unsqueezed = x_ids
            case _:
                raise ValueError("Input dimensions should be either (B, L) or (N, B, L).")

        # z_emb.shape: (N, B[=1], L, D)
        z_emb = self.embedding(x_ids_unsqueezed)

        # z_emb_reshaped.shape: (N * B[=1], L, D)
        z_emb_reshaped = z_emb.view(-1, *z_emb.shape[2:])

        # z_emb_reshaped.shape: (N * B[=1], 1, L, D)
        z_emb_reshaped_unsqueezed = z_emb_reshaped.unsqueeze(1)

        # convs
        # z_convs[i].shape: (N * B[=1], ConvD, L - K + 1)
        z_convs = [conv(z_emb_reshaped_unsqueezed).squeeze(-1) for conv in self.convs]

        # pooling
        # z_pools[i].shape: (N * B[=1], ConvD, 1)
        z_pools = [F.max_pool1d(z_conv, z_conv.shape[2]) for z_conv in z_convs]

        # z_cat.shape: (N * B[=1], ConvD * K))
        z_cat = torch.cat(z_pools, dim=1).squeeze(-1)

        # z_cat_reshaped.shape: (N, [B], ConvD * K)
        z_cat_reshaped = z_cat.view(*x_ids.shape[:-1], -1)

        return z_cat_reshaped
