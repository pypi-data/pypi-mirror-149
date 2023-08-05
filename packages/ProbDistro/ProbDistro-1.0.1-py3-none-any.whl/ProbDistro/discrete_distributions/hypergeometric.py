import ProbDistro.base_discrete_distribution as base_discrete_distribution


class Hypergeometric(base_discrete_distribution.BaseDiscreteDistribution):
    def __init__(self, N: int, K: int, n: int):
        """
        A discrete random variable which can be used to represent the probability of receiving "x" successes in
        "n" dependent draws from a finite population without replacement (draws are not independent of each other)
        from a total population of "N" which contains "K" success states

        :param N: population size
        :param K: number of success states
        :param n: draws/sample size
        """
        self.N = N
        self.K = K
        self.n = n

    def pmf(self, k: int) -> float:
        try:
            return (self._ncr(self.K, k) * self._ncr(self.N - self.K, self.n - k)) / self._ncr(self.N, self.n)
        except ValueError:
            return 0

    def cdf(self, k: int) -> float:
        if k < 0:
            return 0

        return sum(self.pmf(i) for i in range(k + 1))

    def _is_supported(self, x: float) -> bool:
        if isinstance(x, float):
            if not x.is_integer():
                return False

        return max(0, self.n + self.K - self.N) <= x <= min(self.n, self.K)

    def expected_value(self) -> float:
        return self.n * (self.K / self.N)

    def variance(self) -> float:
        return self.n * (self.K / self.N) * ((self.N - self.K) / self.N) * ((self.N - self.n) / (self.N - 1))

    def _get_defaults(self) -> tuple:
        return max(0, self.n + self.K - self.N), min(self.n, self.K), 1
