import ProbDistro.base_discrete_distribution as base_discrete_distribution


class Geometric(base_discrete_distribution.BaseDiscreteDistribution):
    def __init__(self, p: float, include_success_trial: bool = True):
        """
        A discrete random variable which can be used to represent 2 situations.
           1. include_success_trial = True - the number of trials which are needed to obtain exactly 1 success
              supports set {1, 2, 3, 4, ...}
           2. include_success_trial = False - the number of failures before the first success
              supports set {0, 1, 2, 3, ...}

        For example, if the probability is 0.25 for an x value of 3, this indicates there is a 25% chance of receiving
        no successes until the third trial where the first success is obtained

        :param p: probability of success
        """
        self.p = p
        self.q = 1 - p
        self.include_success_trial = include_success_trial

    def pmf(self, x: float) -> float:
        if self.include_success_trial:
            return self.p * self.q ** (x - 1)

        return self.q ** x * self.p

    def cdf(self, x: float) -> float:
        if self.include_success_trial:
            return 1 - (self.q ** x)

        return 1 - (self.q ** (x + 1))

    def _is_supported(self, x: float) -> bool:
        if isinstance(x, float):
            if not x.is_integer():
                return False

        if self.include_success_trial:
            return x >= 1

        return x >= 0

    def expected_value(self) -> float:
        if self.include_success_trial:
            return 1 / self.p

        return self.q / self.p

    def variance(self) -> float:
        return (1 - self.p) / (self.p ** 2)

    def _get_defaults(self) -> tuple:
        if self.include_success_trial:
            return 1, None, 1

        return 0, None, 1
