import math

import ProbDistro.base_discrete_distribution as base_discrete_distribution


class Poisson(base_discrete_distribution.BaseDiscreteDistribution):
    def __init__(self, rate: float):
        """
        A discrete random variable which can be used to represent the probability of "x" events occurring in
        a given time interval, provided they arrive with a mean rate of "rate", and arrivals are independent

        :param rate: Average rate of success
        """
        self.rate = rate

    def pmf(self, x: int) -> float:
        return (self.rate ** x * math.e ** -self.rate) / math.factorial(x)

    def cdf(self, x: int) -> float:
        if x < 0:
            return 0

        return sum(self.pmf(i) for i in range(x + 1))

    def _is_supported(self, x: float) -> bool:
        if isinstance(x, float):
            if not x.is_integer():
                return False

        return x >= 0

    def expected_value(self) -> float:
        return self.rate

    def variance(self) -> float:
        return self.rate

    def _get_defaults(self) -> tuple:
        return 0, None, 1
