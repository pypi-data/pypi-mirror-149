import ProbDistro.base_discrete_distribution as base_discrete_distribution


class Bernoulli(base_discrete_distribution.BaseDiscreteDistribution):
    def __init__(self, p: float):
        """
        A discrete random variable which can be used to represent the outcome of a single yes/no experiment.
        It has a probability of success "p"

        :param p: probability of success
        """
        self.p = p
        self.q = 1 - p

    def pmf(self, x: float) -> float:
        return self.p if x == 1 else self.q

    def cdf(self, x: float) -> float:
        if x < 0:
            return 0

        if 0 <= x < 1:
            return self.q

        return 1

    def _is_supported(self, x: float) -> bool:
        return float(x) in (0, 1)

    def expected_value(self) -> float:
        return self.p

    def variance(self) -> float:
        return self.p * self.q

    def _get_defaults(self) -> tuple:
        return 0, 1, 1
