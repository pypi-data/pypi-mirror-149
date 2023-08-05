import torch
import torch.nn.functional as F

from .univariate_binned import UnivariateBinned
from .generalized_pareto import GeneralizedPareto


class UnivariateSplicedBinnedPareto(UnivariateBinned):
    r"""
    Spliced Binned-Pareto univariate distribution.
    Arguments
    ----------
    bins_lower_bound: The lower bound of the bin edges
    bins_upper_bound: The upper bound of the bin edges
    nbins: The number of equidistance bins to allocate between `bins_lower_bound` and `bins_upper_bound`. Default value is 100.
    percentile_gen_pareto: The percentile of the distribution that is each tail. Default value is 0.05. NB: This symmetric percentile can still represent asymmetric upper and lower tails.
    """

    def __init__(
        self,
        bins_lower_bound: float,
        bins_upper_bound: float,
        nbins: int = 100,
        percentile_gen_pareto: torch.Tensor = torch.tensor(0.05),
        validate_args=None,
    ):
        super().__init__(
            bins_lower_bound, bins_upper_bound, nbins, validate_args
        )

        assert (
            percentile_gen_pareto > 0 and percentile_gen_pareto < 1
        ), "percentile_gen_pareto must be between (0,1)"
        self.percentile_gen_pareto = percentile_gen_pareto

        self.lower_xi = torch.nn.Parameter(torch.tensor(0.5))
        self.lower_beta = torch.nn.Parameter(torch.tensor(0.5))
        self.lower_gen_pareto = GeneralizedPareto(self.lower_xi, self.lower_beta)

        self.upper_xi = torch.nn.Parameter(torch.tensor(0.5))
        self.upper_beta = torch.nn.Parameter(torch.tensor(0.5))
        self.upper_gen_pareto = GeneralizedPareto(self.upper_xi, self.upper_beta)

        self.lower_xi_batch = None
        self.lower_beta_batch = None
        self.upper_xi_batch = None
        self.upper_beta_batch = None

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
        self.logits = self.logits.to(device)

    def forward(self, x):
        """
        Takes input x as the new parameters to specify the bin probabilities: logits for the base distribution, and xi and beta for each tail distribution.
        """
        if len(x.shape) > 1:
            # If mini-batching
            self.logits = x[:, : self.nbins]

            self.lower_xi_batch = F.softplus(x[:, self.nbins])
            self.lower_beta_batch = F.softplus(x[:, self.nbins + 1])

            self.upper_xi_batch = F.softplus(x[:, self.nbins + 2])
            self.upper_beta_batch = F.softplus(x[:, self.nbins + 3])
        else:
            # If not mini-batching
            self.logits = x[: self.nbins]

            self.lower_xi_batch = F.softplus(x[self.nbins])
            self.lower_beta_batch = F.softplus(x[self.nbins + 1])

            self.upper_xi_batch = F.softplus(x[self.nbins + 2])
            self.upper_beta_batch = F.softplus(x[self.nbins + 3])

            self.upper_gen_pareto.xi = self.upper_xi_batch
            self.upper_gen_pareto.beta = self.upper_beta_batch
            self.lower_gen_pareto.xi = self.lower_xi_batch
            self.lower_gen_pareto.beta = self.lower_beta_batch

        return self.logits

    def log_p(self, xx, for_training=True):
        """
        Arguments
        ----------
        xx: one datapoint
        for_training: boolean to indicate a return of the log-probability, or of the loss (which is an adjusted log-probability)
        """
        assert xx.shape.numel() == 1, "log_p() expects univariate"

        # Compute upper and lower tail thresholds at current time from their percentiiles
        upper_percentile = self.icdf(1 - self.percentile_gen_pareto)
        lower_percentile = self.icdf(self.percentile_gen_pareto)

        # Log-prob given binned distribution
        logp_bins = self.log_binned_p(xx) + torch.log(
            1 - 2 * self.percentile_gen_pareto
        )
        logp = logp_bins

        # Log-prob given upper tail distribution
        if xx > upper_percentile:
            if self.upper_xi_batch is not None:
                # self.upper_gen_pareto.xi = torch.square(self.upper_xi_batch[self.idx])
                # self.upper_gen_pareto.beta = torch.square(self.upper_beta_batch[self.idx])
                self.upper_gen_pareto.xi = self.upper_xi_batch[self.idx]
                self.upper_gen_pareto.beta = self.upper_beta_batch[self.idx]
            logp_gen_pareto = self.upper_gen_pareto.log_prob(
                xx - upper_percentile
            ) + torch.log(self.percentile_gen_pareto)
            logp = logp_gen_pareto
            if for_training:
                logp += logp_bins

        # Log-prob given upper tail distribution
        elif xx < lower_percentile:
            if self.lower_xi_batch is not None:
                # self.lower_gen_pareto.xi = torch.square(self.lower_xi_batch[self.idx])
                # self.lower_gen_pareto.beta = torch.square(self.lower_beta_batch[self.idx])
                self.lower_gen_pareto.xi = self.lower_xi_batch[self.idx]
                self.lower_gen_pareto.beta = self.lower_beta_batch[self.idx]
            logp_gen_pareto = self.lower_gen_pareto.log_prob(
                lower_percentile - xx
            ) + torch.log(self.percentile_gen_pareto)
            logp = logp_gen_pareto
            if for_training:
                logp += logp_bins

        return logp

    def cdf_components(self, xx, idx=0, cum_density=torch.tensor([0.0])):
        """
        Cumulative density for one datapoint `xx`, where `cum_density` is the cdf up to bin_edges `idx` which must be lower than `xx`
        """
        bin_cdf_relative = torch.tensor([0.0])
        upper_percentile = self.icdf(1 - self.percentile_gen_pareto)
        lower_percentile = self.icdf(self.percentile_gen_pareto)
        if xx < lower_percentile:
            adjusted_xx = lower_percentile - xx
            cum_density = (
                1.0 - self.lower_gen_pareto.cdf(adjusted_xx)
            ) * self.percentile_gen_pareto
        elif xx <= upper_percentile:
            idx, cum_density, bin_cdf_relative = self.cdf_binned_components(
                xx, idx, cum_density
            )
        else:
            adjusted_xx = xx - upper_percentile
            cum_density = (
                1.0 - self.percentile_gen_pareto
            ) + self.upper_gen_pareto.cdf(
                adjusted_xx
            ) * self.percentile_gen_pareto
        return idx, cum_density, bin_cdf_relative

    def inverse_cdf(self, value):
        """
        Inverse cdf of a single percentile `value`
        """
        assert (
            value >= 0.0 and value <= 1.0
        ), "percentile value must be between 0 and 1 inclusive"

        if value < self.percentile_gen_pareto:
            adjusted_percentile = 1 - (value / self.percentile_gen_pareto)
            icdf_value = self.inverse_binned_cdf(
                self.percentile_gen_pareto
            ) - self.lower_gen_pareto.icdf(adjusted_percentile)
        elif value <= 1 - self.percentile_gen_pareto:
            icdf_value = self.inverse_binned_cdf(value)
        else:
            adjusted_percentile = (
                value - (1.0 - self.percentile_gen_pareto)
            ) / self.percentile_gen_pareto
            icdf_value = self.upper_gen_pareto.icdf(
                adjusted_percentile
            ) + self.inverse_binned_cdf(1 - self.percentile_gen_pareto)

        return icdf_value