import abc
import math
import typing


class BaseDistribution(abc.ABC):
    @abc.abstractmethod
    def cdf(self, x: float) -> float:
        pass

    @abc.abstractmethod
    def equals(self, x: float) -> float:
        pass

    @abc.abstractmethod
    def _is_supported(self, x: float) -> bool:
        pass

    @abc.abstractmethod
    def expected_value(self) -> float:
        pass

    @abc.abstractmethod
    def variance(self) -> float:
        pass

    @abc.abstractmethod
    def less_than(self, x: float) -> float:
        pass

    @abc.abstractmethod
    def less_than_equals(self, x: float) -> float:
        pass

    @abc.abstractmethod
    def greater_than(self, x: float) -> float:
        pass

    @abc.abstractmethod
    def greater_than_equals(self, x: float) -> float:
        pass

    def __call__(self, x: float) -> float:
        return self.equals(x)

    def __repr__(self):
        return "<{}Distribution {}>".format(self.__class__.__name__, self._format_variables())

    def mean(self) -> float:
        return self.expected_value()

    def standard_deviation(self) -> float:
        return math.sqrt(self.variance())

    @abc.abstractmethod
    def between(self, upper: float, lower: float):
        pass

    def _check_supported(self, x: float):
        if self._is_supported(x):
            return

        raise ValueError("x={} is not supported by this distribution!".format(x))

    def _format_variables(self) -> str:
        return " ".join("{}={}".format(k, v) for k, v in self.__dict__.items())

    @staticmethod
    def _ncr(n: int, r: int) -> int:
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

    @staticmethod
    def _npr(n: int, r: int) -> int:
        return math.factorial(n) // math.factorial(n - r)

    def _equals_range(self, x: typing.Iterable, caller: callable) -> list:
        return [caller(i) for i in x]

    def cdf_range(self, x: typing.Iterable):
        return self._equals_range(x, self.cdf)
