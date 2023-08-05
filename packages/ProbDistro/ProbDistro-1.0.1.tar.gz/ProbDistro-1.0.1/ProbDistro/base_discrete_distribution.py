import abc
import typing

import ProbDistro.base_distribution as base_distribution
if typing.TYPE_CHECKING:
    import ProbDistro.discrete_distributions.discrete_random_variable as discrete_random_variable


class BaseDiscreteDistribution(base_distribution.BaseDistribution, abc.ABC):
    @abc.abstractmethod
    def pmf(self, x: float) -> float:
        pass

    def equals(self, x: float) -> float:
        self._check_supported(x)
        return self.pmf(x)

    def less_than(self, x: float) -> float:
        self._check_supported(x)
        return self.cdf(x) - self.equals(x)

    def less_than_equals(self, x: float) -> float:
        self._check_supported(x)
        return self.cdf(x)

    def greater_than(self, x: float) -> float:
        self._check_supported(x)
        return 1 - self.less_than_equals(x)

    def greater_than_equals(self, x: float) -> float:
        self._check_supported(x)
        return 1 - self.less_than(x)

    def between(self, upper: float, lower: float):
        return self.equals(upper) - self.equals(lower)

    def pmf_range(self, x: typing.Iterable):
        return self._equals_range(x, self.pmf)

    @abc.abstractmethod
    def _get_defaults(self) -> tuple:
        pass

    def to_discrete_random_variable(
            self, start: float = None, stop: float = None, step: float = None
    ) -> 'discrete_random_variable.DiscreteRandomVariable':

        import ProbDistro.discrete_distributions.discrete_random_variable as drv

        default_start, default_stop, default_step = self._get_defaults()

        start = default_start if start is None else start
        stop = default_stop if stop is None else stop
        step = default_step if step is None else step

        if start is None:
            raise ValueError("Starting value must be explicitly set")

        if stop is None:
            raise ValueError("Stopping value must be explicitly set")

        if step is None:
            raise ValueError("Step value must be explicitly set")

        x = []
        px = []

        i = start
        while i <= stop:
            x.append(i)
            px.append(self.equals(i))

            i += step

        return drv.DiscreteRandomVariable.correct_probabilities(x, px)
