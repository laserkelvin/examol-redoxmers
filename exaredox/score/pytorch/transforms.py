# Copyright (C) 2023 Intel Corporation
# SPDX-License-Identifier: MIT License

"""Data transformation"""
import torch
from torch_geometric.data import Data

__all__ = ["MeanScaler"]


class MeanScaler:
    """
    Class for rescaling target labels. More or less treats the same way
    as you would with the ``StandardScaler`` class in `sklearn.preprocessing`.

    Also implements the inverse, where we rescale model predictions to 'real'
    values.
    """

    def __init__(self, mean: float, var: float, epsilon: float = 1e-7) -> None:
        self.mean = mean
        self.var = var
        self.epsilon = epsilon

    def __call__(self, molecule: Data) -> Data:
        target = molecule.target
        target = (target - self.mean) / (self.var + self.epsilon)
        molecule.target = target
        return molecule

    def inverse_transform(self, predictions: torch.Tensor) -> torch.Tensor:
        return (predictions * self.var) + self.mean
