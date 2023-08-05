from numbers import Number

import torch
from torch.distributions import constraints
from torch.distributions.distribution import Distribution
from torch.distributions.utils import broadcast_all
from typing import Dict
import numpy as np


class GeneralizedPareto(Distribution):

    def __init__(self, xi, beta, validate_args=None):
        """Generalised Pareto distribution.

        Args:
            xi (torch.Tensor): Tensor containing the xi (heaviness) shape parameters
            beta (torch.Tensor): Tensor containing the xi (heaviness) shape parameters
            validate_args (bool):
        """
        self.xi, self.beta = broadcast_all(xi, beta)

        if isinstance(xi, Number) and isinstance(beta, Number):
            batch_shape = torch.Size()
        else:
            batch_shape = self.xi.size()
        super(GeneralizedPareto, self).__init__(
            batch_shape, validate_args=validate_args
        )

        if (
            self._validate_args
            and not torch.lt(-self.beta, torch.zeros_like(self.beta)).all()
        ):
            raise ValueError("GenPareto is not defined when scale beta<=0")

    @property
    def arg_constraints(self) -> Dict[str, constraints.Constraint]:
        constraint_dict = {
            "xi": constraints.positive,
            "beta": constraints.positive,
        }
        return constraint_dict

    @property
    def mean(self):
        mu = torch.where(
            self.xi < 1,
            torch.div(self.beta, 1 - self.xi),
            np.nan * torch.ones_like(self.xi),
        )
        return mu

    @property
    def variance(self):
        xi, beta = self.xi, self.beta
        return torch.where(
            xi < 1 / 2.0,
            torch.div(beta ** 2, torch.mul((1 - xi) ** 2, (1 - 2 * xi))),
            np.nan * torch.ones_like(xi),
        )

    @property
    def stddev(self):
        return torch.sqrt(self.variance)

    def log_prob(self, x):
        if self.xi == 0:
            logp = -self.beta.log() - x / self.beta
        else:
            logp = -self.beta.log() - (1 + 1.0 / (self.xi + 1e-6)) * torch.log(
                1 + self.xi * x / self.beta
            )
        return torch.where(
            x < torch.zeros_like(x), -np.inf * torch.ones_like(x), logp
        )

    def cdf(self, x):
        x_shifted = torch.div(x, self.beta)
        u = 1 - torch.pow(1 + self.xi * x_shifted, -torch.reciprocal(self.xi))
        return u

    def icdf(self, value):
        x_shifted = torch.div(torch.pow(1 - value, -self.xi) - 1, self.xi)
        x = torch.mul(x_shifted, self.beta)
        return x