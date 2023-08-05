import math

import ProbDistro.base_continuous_distribution as base_continuous_distribution


class Exponential(base_continuous_distribution.BaseContinuousDistribution):
    def __init__(self, rate: float):
        """
        A continuous random variable representing the probability of time between events of a Poisson distribution
        (Occurs independently, continuously, and at an average rate)

        It is also memoryless

        :param rate: the average rate of arrivals
        """
        self.rate = rate

    def pdf(self, x: float) -> float:
        return self.rate * math.e ** (-self.rate * x)

    def cdf(self, x: float) -> float:
        return 1 - math.e ** (-self.rate * x)

    def expected_value(self) -> float:
        return 1 / self.rate

    def variance(self) -> float:
        return 1 / (self.rate ** 2)

    def _is_supported(self, x: float) -> bool:
        return x >= 0
