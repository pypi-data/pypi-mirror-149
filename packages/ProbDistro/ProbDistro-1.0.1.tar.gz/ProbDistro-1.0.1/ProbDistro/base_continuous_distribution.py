import abc
import typing

import ProbDistro.base_distribution as base_distribution


class BaseContinuousDistribution(base_distribution.BaseDistribution, abc.ABC):
    @abc.abstractmethod
    def pdf(self, x: float) -> float:
        pass

    def equals(self, x: float) -> float:
        return 0

    def _is_supported(self, x: float) -> bool:
        return True

    def less_than(self, x: float) -> float:
        self._check_supported(x)
        return self.cdf(x)

    def less_than_equals(self, x: float) -> float:
        self._check_supported(x)
        return self.cdf(x)

    def greater_than(self, x: float) -> float:
        self._check_supported(x)
        return 1 - self.cdf(x)

    def greater_than_equals(self, x: float) -> float:
        self._check_supported(x)
        return 1 - self.cdf(x)

    def between(self, upper: float, lower: float):
        return self.less_than_equals(upper) - self.less_than_equals(lower)

    def pdf_range(self, x: typing.Iterable):
        return self._equals_range(x, self.pdf)
