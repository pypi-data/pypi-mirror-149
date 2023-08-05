import math

import ProbDistro.base_continuous_distribution as base_continuous_distribution


class Normal(base_continuous_distribution.BaseContinuousDistribution):
    def __init__(self, mean: float, variance: float):
        """
         A continuous random variable representing a bell curve distribution, which is ubiquitous.

        :param mean: the mean of the distribution
        :param variance: the variance of the distribution
        """
        self.mu = mean
        self.sigma = variance

    def pdf(self, x: float) -> float:
        a = 1 / (self.sigma * math.sqrt(2 * math.pi))
        b = -0.5 * ((x - self.mu) / self.sigma) ** 2

        return a * math.e ** b

    def cdf(self, x: float) -> float:
        return 0.5 * (1 + math.erf((x - self.mu) / (self.sigma * math.sqrt(2))))

    def expected_value(self) -> float:
        return self.mu

    def variance(self) -> float:
        return self.sigma ** 2
