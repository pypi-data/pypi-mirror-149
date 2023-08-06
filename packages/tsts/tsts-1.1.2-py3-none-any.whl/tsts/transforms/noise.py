import random
from typing import Optional

from torch import Tensor
from torch.autograd import Variable
from tsts.core import TRANSFORMS
from tsts.types import Frame

from .transform import Transform


@TRANSFORMS.register()
class GaussianNoise(Transform):
    """Add gaussian noise to input."""

    def __init__(
        self,
        mean: float = 0.0,
        std: float = 0.001,
        p: float = 0.5,
    ) -> None:
        self.mean = mean
        self.std = std
        self.p = p

    def apply(
        self,
        X: Tensor,
        y: Optional[Tensor] = None,
        bias: Optional[Tensor] = None,
        time_stamps: Optional[Tensor] = None,
    ) -> Frame:
        if random.random() < self.p:
            data = X.data.new(X.size()).normal_(self.mean, self.std)
            noise = Variable(data)
            X = X + noise
        return (X, y, bias, time_stamps)
