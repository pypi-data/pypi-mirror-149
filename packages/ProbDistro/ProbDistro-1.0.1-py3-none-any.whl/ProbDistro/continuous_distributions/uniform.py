import ProbDistro.base_continuous_distribution as base_continuous_distribution


class Uniform(base_continuous_distribution.BaseContinuousDistribution):
    def __init__(self, a: float, b: float):
        """
         A continuous random variable representing equally likely outcomes between "a" and "b"

         If "a" and "b" are backwards, they will automatically be corrected

        :param a: lower bound
        :param b: upper bound
        """
        self.a = min(a, b)
        self.b = max(a, b)

    def pdf(self, x: float) -> float:
        if self.a <= x <= self.b:
            return 1 / (self.b - self.a)

        return 0

    def cdf(self, x: float) -> float:
        if x < self.a:
            return 0

        if self.a <= x <= self.b:
            return (x - self.a) / (self.b - self.a)

        return 1

    def expected_value(self) -> float:
        return 0.5 * (self.a + self.b)

    def variance(self) -> float:
        return 1 / 12 * (self.b - self.a) ** 2
