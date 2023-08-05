import torch
import torch.nn.functional as F
from typing import List, Union, Optional
import numpy as np


class UnivariateBinned(torch.nn.Module):
    r"""
    Binned univariate distribution designed as an nn.Module
    Arguments
    ----------
    bins_lower_bound: The lower bound of the bin edges
    bins_upper_bound: The upper bound of the bin edges
    nbins: The number of equidistant bins to allocate between `bins_lower_bound` and `bins_upper_bound`. Default value is 100.
    smoothing_indicator: The method of smoothing to perform on the bin probabilities
    """

    def __init__(
        self,
        bins_lower_bound: float,
        bins_upper_bound: float,
        nbins: int = 100,
        smoothing_indicator: Optional[str] = [None, "cheap", "kernel"][1],
        validate_args=None,
    ):
        super().__init__()

        assert (
            bins_lower_bound.shape.numel() == 1
        ), f"bins_lower_bound needs to have shape torch.Size([1])"
        assert (
            bins_upper_bound.shape.numel() == 1
        ), f"bins_upper_bound needs to have shape torch.Size([1])"
        assert (
            bins_lower_bound < bins_upper_bound
        ), f"bins_lower_bound {bins_lower_bound} needs to less than bins_upper_bound {bins_upper_bound}"

        self.nbins = nbins
        self.epsilon = np.finfo(np.float32).eps
        self.smooth_indicator = smoothing_indicator

        # Creation the bin locations
        # Bins locations are placed uniformly between bins_lower_bound and bins_upper_bound, though more complex methods could be used
        self.bin_min = bins_lower_bound - self.epsilon * 6
        self.bin_max = bins_upper_bound + self.epsilon * 6
        self.bin_edges = torch.linspace(self.bin_min, self.bin_max, nbins + 1)
        self.bin_widths = self.bin_edges[1:] - self.bin_edges[:-1]
        self.bin_centres = (self.bin_edges[1:] + self.bin_edges[:-1]) * 0.5

        logits = torch.ones(nbins)
        logits = (
            logits / logits.sum() / (1 + self.epsilon) / self.bin_widths.mean()
        )
        self.logits = torch.log(logits)

        # Keeps track of mini-batches
        self.idx = None

        self.device = None

    def to_device(self, device):
        """
        Moves members to a specified torch.device
        """
        self.device = device
        self.bin_min = self.bin_min.to(device)
        self.bin_max = self.bin_max.to(device)
        self.bin_edges = self.bin_edges.to(device)
        self.bin_widths = self.bin_widths.to(device)
        self.bin_centres = self.bin_centres.to(device)

    def forward(self, x):
        """
        Takes input x as new logits
        """
        self.logits = x
        return self.logits

    def log_bins_prob(self):
        if self.idx is None:
            log_bins_prob = F.log_softmax(self.logits, dim=0).sub(
                torch.log(self.bin_widths)
            )
        else:
            log_bins_prob = F.log_softmax(self.logits[self.idx, :], dim=0).sub(
                torch.log(self.bin_widths)
            )
        return log_bins_prob.float()

    def bins_prob(self):
        bins_prob = self.log_bins_prob().exp()
        return bins_prob

    def bins_cdf(self):
        incomplete_cdf = self.bins_prob().mul(self.bin_widths).cumsum(dim=0)
        zero = 0 * incomplete_cdf[0].view(1)  # ensured to be on same device
        return torch.cat((zero, incomplete_cdf))

    def log_binned_p(self, xx):
        """
        Log probability for one datapoint.
        """
        assert xx.shape.numel() == 1, "log_binned_p() expects univariate"

        # Transform xx in to a one-hot encoded vector to get bin location
        vect_above = xx - self.bin_edges[1:]
        vect_below = self.bin_edges[:-1] - xx
        one_hot_bin_indicator = (vect_above * vect_below >= 0).float()

        if xx > self.bin_edges[-1]:
            one_hot_bin_indicator[-1] = 1.0
        elif xx < self.bin_edges[0]:
            one_hot_bin_indicator[0] = 1.0
        if not (one_hot_bin_indicator == 1).sum() == 1:
            print(
                f"Warning in log_p(self, xx): for xx={xx.item()}, one_hot_bin_indicator value_counts are {one_hot_bin_indicator.unique(return_counts=True)}"
            )

        if self.smooth_indicator == "kernel":
            # The kernel variant is better but slows down training quite a bit
            idx_one_hot = torch.argmax(one_hot_bin_indicator)
            kernel = [0.006, 0.061, 0.242, 0.383, 0.242, 0.061, 0.006]
            len_kernel = len(kernel)
            for i in range(len_kernel):
                idx = i - len_kernel // 2 + idx_one_hot
                if idx in range(len(one_hot_bin_indicator)):
                    one_hot_bin_indicator[idx] = kernel[i]

        elif self.smooth_indicator == "cheap":
            # This variant is cheaper in computation time
            idx_one_hot = torch.argmax(one_hot_bin_indicator)
            if not idx_one_hot + 1 >= len(one_hot_bin_indicator):
                one_hot_bin_indicator[idx_one_hot + 1] = 0.5
            if not idx_one_hot - 1 < 0:
                one_hot_bin_indicator[idx_one_hot - 1] = 0.5
            if not idx_one_hot + 2 >= len(one_hot_bin_indicator):
                one_hot_bin_indicator[idx_one_hot + 2] = 0.25
            if not idx_one_hot - 2 < 0:
                one_hot_bin_indicator[idx_one_hot - 2] = 0.25

        logp = torch.dot(one_hot_bin_indicator, self.log_bins_prob())
        return logp

    def log_p(self, xx):
        """
        Log probability for one datapoint `xx`.
        """
        assert xx.shape.numel() == 1, "log_p() expects univariate"
        return self.log_binned_p(xx)

    def log_prob(self, x):
        """
        Log probability for a tensor of datapoints `x`.
        """
        x = x.view(x.shape.numel())
        self.idx = 0
        if x.shape[0] == 1:
            self.idx = None
        lpx = self.log_p(x[0]).view(1)

        if x.shape.numel() == 1:
            return lpx

        for xx in x[1:]:
            self.idx += 1
            lpxx = self.log_p(xx).view(1)
            lpx = torch.cat((lpx, lpxx), 0)

        self.idx = None
        return lpx

    def cdf_binned_components(
        self, xx, idx=0, cum_density=torch.tensor([0.0])
    ):
        """
        Cumulative density given bins for one datapoint `xx`, where `cum_density` is the cdf up to bin_edges `idx`  which must be lower than `xx`
        """
        assert xx.shape.numel() == 1, "cdf_components() expects univariate"

        bins_range = self.bin_edges[-1] - self.bin_edges[0]
        bin_cdf_relative = torch.tensor([0.0])
        if idx == 0:
            cum_density = torch.tensor([0.0])

        while xx > self.bin_edges[idx] and idx < self.nbins:
            bin_width = self.bin_edges[idx + 1] - self.bin_edges[idx]
            if xx < self.bin_edges[idx + 1]:
                bin_cdf = torch.distributions.uniform.Uniform(
                    self.bin_edges[idx], self.bin_edges[idx + 1]
                ).cdf(xx)
                bin_cdf_relative = bin_cdf * bin_width / bins_range
                break
            else:
                cum_density += self.bins_prob()[idx] * bin_width
                idx += 1
        return idx, cum_density, bin_cdf_relative

    def cdf_components(self, xx, idx=0, cum_density=torch.tensor([0.0])):
        """
        Cumulative density for one datapoint `xx`, where `cum_density` is the cdf up to bin_edges `idx` which must be lower than `xx`
        """
        return self.cdf_binned_components(xx, idx, cum_density)

    def cdf(self, x):
        """
        Cumulative density tensor for a tensor of datapoints `x`.
        """
        x = x.view(x.shape.numel())
        sorted_x = x.sort()
        x, unsorted_index = sorted_x.values, sorted_x.indices

        idx, cum_density, bin_cdf_relative = self.cdf_components(
            x[0], idx=0, cum_density=torch.tensor([0.0])
        )
        cdf_tensor = (cum_density + bin_cdf_relative).view(1)
        if x.shape.numel() == 1:
            return cdf_tensor

        for xx in x[1:]:
            idx, cum_density, bin_cdf_relative = self.cdf_components(
                xx, idx, cum_density
            )
            cdfx = (cum_density + bin_cdf_relative).view(1)
            cdf_tensor = torch.cat((cdf_tensor, cdfx), 0)

        cdf_tensor = cdf_tensor[unsorted_index]
        return cdf_tensor

    def inverse_binned_cdf(self, value):
        """
        Inverse binned cdf of a single quantile `value`
        """
        assert (
            value.shape.numel() == 1
        ), "inverse_binned_cdf() expects univariate"
        if value == 0.0:
            return self.bin_edges[0]
        if value == 1:
            return self.bin_edges[-1]

        vect_above = value - self.bins_cdf()[1:]
        vect_below = self.bins_cdf()[:-1] - value

        if (vect_above == 0).any():
            result = self.bin_edges[1:][vect_above == 0]
        elif (vect_below == 0).any():
            result = self.bin_edges[:-1][vect_below == 0]
        else:
            one_hot_edge_indicator = vect_above * vect_below >= 0  # .float()
            low = self.bin_edges[:-1][one_hot_edge_indicator]
            high = self.bin_edges[1:][one_hot_edge_indicator]
            value_relative = (
                value - self.bins_cdf()[:-1][one_hot_edge_indicator]
            )
            result = torch.distributions.uniform.Uniform(low, high).icdf(
                value_relative
            )

        return result

    def inverse_cdf(self, value):
        """
        Inverse cdf of a single percentile `value`
        """
        return self.inverse_binned_cdf(value)

    def icdf(self, values):
        """
        Inverse cdf of a tensor of quantile `values`
        """
        if self.device is not None:
            values = values.to(self.device)

        values = values.view(values.shape.numel())
        icdf_tensor = self.inverse_cdf(values[0])
        icdf_tensor = icdf_tensor.view(1)

        if values.shape.numel() == 1:
            return icdf_tensor

        for value in values[1:]:
            icdf_value = self.inverse_cdf(value).view(1)
            icdf_tensor = torch.cat((icdf_tensor, icdf_value), 0)

        return icdf_tensor