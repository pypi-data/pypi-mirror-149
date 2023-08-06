# references
# https://kornia.readthedocs.io/en/latest/_modules/kornia/losses/focal.html


import torch
import torch.nn as nn
import torch.nn.functional as F


class FocalLoss(nn.Module):
    """Focal Loss

    - https://arxiv.org/abs/1708.02002/

    Args:
        num_classes (int):
        alpha (float):
        gamma (float):
        reduction (str):
    """

    def __init__(
        self,
        num_classes: int,
        alpha: float,
        gamma: float = 2.0,
        reduction: str = "none",
    ) -> None:
        super(FocalLoss, self).__init__()

        self.num_classes: int = num_classes
        self.alpha: float = alpha
        self.gamma: float = gamma
        self.reduction: str = reduction

    def forward(
        self,
        y_pred: torch.Tensor,
        y_true: torch.Tensor,
    ) -> torch.Tensor:
        """TODO

        Args:
            y_pred (torch.Tensor):
            y_true (torch.Tensor):

        Returns:
            loss (torch.Tensor):
        """
        # convert y_true to one-hot encoding
        y_true_one_hot = F.one_hot(y_true, self.num_classes).type(y_pred.dtype)

        # softmax(y_pred) and log(softmax(y_pred))
        softmax_y_pred = F.softmax(y_pred, dim=-1)
        log_softmax_y_pred = F.log_softmax(y_pred, dim=-1)

        focal = -self.alpha * torch.pow(1.0 - softmax_y_pred, self.gamma) * log_softmax_y_pred
        loss = torch.einsum("ab...,ab...->a...", (y_true_one_hot, focal))

        match self.reduction:
            case "none":
                return loss
            case "mean":
                return torch.mean(loss)
            case "sum":
                return torch.sum(loss)
            case _:
                raise ValueError
