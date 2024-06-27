from typing import Callable, Iterable, Union

import numpy as np
import torch

Matrix = Union[np.ndarray, torch.Tensor]


class SlidingWindow2d:
    def __init__(
        self,
        func: Callable[
            [Iterable],
            Iterable,
        ],
        size: Union[tuple[int, int], int] = (3, 3),
        stride: Union[tuple[int, int], int] = 1,
        # values: Matrix = None,
    ):
        self.size = size
        self.stride = stride
        self.mat: Union[None, Matrix] = None
        self.func = func

    def set_mat(self, mat: Matrix):
        if mat is None:
            raise ValueError("mat should be a Matrix")
        self.mat = mat

    def __call__(self, mat: Matrix) -> Matrix:
        if self.mat is None:
            raise ValueError("Values is None")
        if len(mat.shape) not in (1, 3):
            raise ValueError("Matrix must be 1d or 3d")
        return mat
