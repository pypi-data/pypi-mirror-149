import math
import typing
import ProbDistro.base_discrete_distribution as base_discrete_distribution


class DiscreteRandomVariable(base_discrete_distribution.BaseDiscreteDistribution):
    def __init__(self, x: typing.Sequence[float], px: typing.Sequence[float]):
        if round(sum(px), 10) != 1:
            raise ValueError(
                "Sum of all probabilities must equal 1 by law of total probability. Got {}.".format(sum(px))
            )

        if len(x) != len(px):
            raise ValueError("There are {} x values, but {} probabilities. These counts must match.".format(
                len(x), len(px)
            ))

        self.x = list(x)
        self.px = list(px)

    @classmethod
    def from_dict(cls, data: dict, correct: bool = False):
        keys = list(data.keys())
        keys.sort()

        values = []

        for k in keys:
            values.append(data[k])

        if correct:
            return cls.correct_probabilities(keys, values)

        return cls(keys, values)

    @classmethod
    def correct_probabilities(cls, x: typing.Sequence[float], px: typing.Sequence[float]):
        denominator = sum(px)
        px = [i / denominator for i in px]

        return cls(x, px)

    def __pow__(self, power, modulo=None) -> 'DiscreteRandomVariable':
        return DiscreteRandomVariable([x ** power for x in self.x], self.px)

    def __mul__(self, other: 'DiscreteRandomVariable') -> 'DiscreteRandomVariable':
        result = {}

        for x, px in zip(self.x, self.px):
            for y, py in zip(other.x, other.px):
                if x * y not in result:
                    result[x * y] = self.p_and(px, py)

                else:
                    result[x * y] += self.p_and(px, py)

        return DiscreteRandomVariable.from_dict(result)

    def pmf(self, x: float) -> float:
        return self.px[self.x.index(x)]

    def cdf(self, x: float) -> float:
        total = 0
        for i in range(len(self.x)):
            if self.x[i] <= x:
                total += self.px[i]

        return total

    def _is_supported(self, x: float) -> bool:
        return x in self.x

    def expected_value(self) -> float:
        return sum(a * b for a, b in zip(self.x, self.px))

    def variance(self) -> float:
        return (self ** 2).expected_value() - self.expected_value() ** 2

    @staticmethod
    def p_and(x: float, other: float):
        return x * other

    @staticmethod
    def p_or(x: float, other: float):
        return (x + other) - (x * other)

    @staticmethod
    def p_disjoint_or(x: float, other: float):
        return x + other

    @staticmethod
    def p_given(x: float, other: float):
        return (x * other) / x

    @staticmethod
    def intersection(x: float, other: float):
        return DiscreteRandomVariable.p_and(x, other)

    @staticmethod
    def union(x: float, other: float):
        return DiscreteRandomVariable.p_or(x, other)

    @staticmethod
    def disjoint_union(x: float, other: float):
        return DiscreteRandomVariable.p_disjoint_or(x, other)

    def jointly_distributed_table(self, other: 'DiscreteRandomVariable') -> typing.List[typing.List[float]]:
        result = []

        for y in other.px:
            result.append([])
            for x in self.px:
                result[-1].append(self.p_and(x, y))

        return result

    def _get_defaults(self) -> tuple:
        return min(self.x), max(self.x), 1

    def to_discrete_random_variable(
            self, start: float = None, stop: float = None, step: float = None
    ) -> 'DiscreteRandomVariable':

        default_start, default_stop, default_step = self._get_defaults()

        start = default_start if start is None else start
        stop = default_stop if stop is None else stop

        res_x = []
        res_px = []

        for x, px in zip(self.x, self.px):
            if start <= x <= stop:
                res_x.append(x)
                res_px.append(px)

        return DiscreteRandomVariable.correct_probabilities(res_x, res_px)

    def covariance(self, other: 'DiscreteRandomVariable') -> float:
        return (self * other).expected_value() - (self.expected_value() * other.expected_value())

    def correlation(self, other: 'DiscreteRandomVariable') -> float:
        return self.covariance(other) / math.sqrt(self.variance() * other.variance())
