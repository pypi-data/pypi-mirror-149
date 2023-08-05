import ProbDistro.base_discrete_distribution as base_discrete_distribution
import ProbDistro.discrete_distributions.poisson as poisson


class Binomial(base_discrete_distribution.BaseDiscreteDistribution):
    def __init__(self, n: int, p: float):
        """
        A discrete random variable which can be used to represent the outcome of "n" yes/no experiments
        With "p" probability of success, and "1 - p" probability of failure

        :param n: number of trials
        :param p: probability of success
        """
        self.n = n
        self.p = p
        self.q = 1 - p

    def pmf(self, x: int) -> float:
        return self._ncr(self.n, x) * self.p ** x * self.q ** (self.n - x)

    def cdf(self, x: int) -> float:
        if x < 0:
            return 0

        if 0 <= x <= self.n:
            return sum(self.pmf(i) for i in range(x + 1))

        return 1

    def _is_supported(self, x: float) -> bool:
        if isinstance(x, float):
            if not x.is_integer():
                return False

        return 0 <= x <= self.n

    def expected_value(self) -> float:
        return self.n * self.p

    def variance(self) -> float:
        return self.n * self.p * self.q

    def as_poisson(self) -> poisson.Poisson:
        return poisson.Poisson(self.n * self.p)

    def _get_defaults(self) -> tuple:
        return 0, self.n, 1
