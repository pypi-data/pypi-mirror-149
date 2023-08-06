from typing import List, Tuple, Any

import numpy as np
import scipy.stats as st


def confidence_interval(values: List[float], alpha: float = 0.95) -> Tuple[float, float]:
    """ Obtain the maximum and minimum value of a confidence interval for a given alpha value
      from a list of values.

    :param values: A list of values.
    :param alpha: The alpha value of a coefficient interval in a value between 0 and 1.
    :return: The minimum and maximum values.
    """
    a, b = st.t.interval(alpha, len(values) - 1, loc=np.mean(values), scale=st.sem(values))
    return a, b


def interval2score(a: float, b: float) -> Tuple[float, float]:
    """ Convert a confidence interval represented by the minimum and maximum values to a tuple with
      the mean value and the confidence interval (v±ci).

    :param a: One limit value.
    :param b: The other limit value.
    :return: A tuple (v, ci) that represents v±ci where v is the value and ci is the confidence interval.
    """
    return (b + a) / 2, (max(a, b) - min(b, a)) / 2


def confidence_score(values: List[float], alpha: float = 0.95) -> Tuple[float, float]:
    """ Obtain the mean and the confidence interval that represents v±ci.

    :param values: A list of values.
    :param alpha: The alpha value of a coefficient interval in a value between 0 and 1.
    :return: A tuple (v, ci) that represents v±ci where v is the mean value and ci is the confidence interval for that
       alpha.
    """
    return interval2score(*confidence_interval(values, alpha))


class CI(object):
    """ Class that represents a value with a confidence interval. """
    @property
    def value(self) -> float:
        """ The mean value. """
        return self.__value

    @property
    def ci(self) -> float:
        """ The confidence interval (±ci). """
        return self.__ci

    @property
    def p(self) -> float:
        """ The p value. """
        return self.__p

    @property
    def alpha(self) -> float:
        """ The alpha value. """
        return 1 - self.__p

    @property
    def min(self) -> float:
        """ The minimum value of the confidence interval. """
        return self.__value - self.__ci

    @property
    def max(self) -> float:
        """ The maximum value of the confidence interval. """
        return self.__value + self.__ci

    @property
    def interval(self) -> Tuple[float, float]:
        """ The minimum and maximum values of the confidence interval. """
        return self.min, self.max

    def __init__(self, value: float, ci: float, p: float = None) -> None:
        """ Constructor.

        :param value: The mean value.
        :param ci: The interval confidence that represents value±ci.
        :param p: The p value for that confidence interval.
        """
        self.__value = value
        self.__ci = abs(ci)
        self.__p = p

    @staticmethod
    def confidence_score(values: List[float], alpha: float = 0.95) -> 'CI':
        """ Obtain the mean value and confidence interval for a list of measures for different metrics.

        :param values: A list of values.
        :param alpha: The alpha value of a coefficient interval in a value between 0 and 1.
        :return: A dictionary with the different metrics and a tuple with the mean value and the confidence interval.
        """
        a, b = confidence_interval(values, alpha)
        return CI.from_interval(a, b, 1 - alpha)

    @staticmethod
    def from_interval(a: float, b: float, p: float = None) -> 'CI':
        """ Generate a value with confidence intervals from the minimum and maximum values of the confidence interval.

        :param a: One of the limit values of the confidence interval.
        :param b: The other limit value of the confidence interval.
        :param p: The p value.
        :return: A CI object.
        """
        return CI(*interval2score(a, b), p)

    def is_significant(self, other: 'CI') -> bool:
        """ Check if two values with confidence intervals are significant.

        :param other: The other value with confidence intervals.
        :return: True if the value are significantly different.
        """
        return self.value + self.ci < other.value - other.ci or self.value - self.ci > other.value + other.ci

    def is_equivalent(self, other: 'CI') -> bool:
        """ Check if two values with confidence intervals are equivalents, that means, are not statistically different.

        :param other: The other value with confidence intervals.
        :return: True if the value are not significantly different.
        """
        return not self.is_significant(other)

    def is_gt(self, other: 'CI') -> bool:
        """ If this value is greater than other value with confidence intervals.

        :param other: The other value with confidence intervals.
        :return: True if this value is significantly greater than the other.
        """
        return self.value - self.ci > other.value + other.ci

    def is_ge(self, other: 'CI') -> bool:
        """ If this value is greater or equal than other value with confidence intervals.

        :param other: The other value with confidence intervals.
        :return: True if this value is significantly greater or equal than the other.
        """
        return self.value - self.ci >= other.value + other.ci

    def is_lt(self, other: 'CI') -> bool:
        """ If this value is lower than other value with confidence intervals.

        :param other: The other value with confidence intervals.
        :return: True if this value is significantly lower than the other.
        """
        return self.value - self.ci < other.value + other.ci

    def is_le(self, other: 'CI') -> bool:
        """ If this value is lower or equal than other value with confidence intervals.

        :param other: The other value with confidence intervals.
        :return: True if this value is significantly lower or equal than the other.
        """
        return self.value - self.ci <= other.value + other.ci

    def __repr__(self) -> str:
        """ A string representation of this confidence interval. """
        return f'CI({self.__value}, {self.__ci})'

    def __str__(self) -> str:
        """ A string representation of this confidence interval. """
        return f'{self.__value}±{self.__ci}'

    def __iter__(self):
        """ A iterable over the mean and the confidence interval. """
        return iter((self.__value, self.__ci))

    def __eq__(self, other: Any) -> bool:
        """ If the mean value of this confidence interval is exactly the same that other float value.

        :param other: Any float representation object.
        :return: True if the mean of this confidence interval is exactly the same that the other value.
        """
        return self.value == float(other)

    def __ne__(self, other: Any) -> bool:
        """ If the mean value of this confidence interval is not exactly the same that other float value.

        :param other: Any float representation object.
        :return: True if the mean of this confidence interval is not exactly the same that the other value.
        """
        return self.value != float(other)

    def __gt__(self, other: Any) -> bool:
        """ If the mean value of this confidence interval is greater than other float value.

        :param other: Any float representation object.
        :return: True if the mean of this confidence interval is greater than the other value.
        """
        return self.value > float(other)

    def __lt__(self, other: Any) -> bool:
        """ If the mean value of this confidence interval is lower than other float value.

        :param other: Any float representation object.
        :return: True if the mean of this confidence interval is lower than the other value.
        """
        return self.value < float(other)

    def __ge__(self, other: Any) -> bool:
        """ If the mean value of this confidence interval is greater or equal than other float value.

        :param other: Any float representation object.
        :return: True if the mean of this confidence interval is greater or equal than the other value.
        """
        return self.value >= float(other)

    def __le__(self, other: Any) -> bool:
        """ If the mean value of this confidence interval is lower or equal than other float value.

        :param other: Any float representation object.
        :return: True if the mean of this confidence interval is lower or equal than the other value.
        """
        return self.value <= float(other)

    def __bool__(self) -> bool:
        """ True if this value and the interval confidence are different to zero, otherwise False. """
        return bool(self.value) or bool(self.ci)

    def __float__(self) -> float:
        """ The mean value of the confidence interval. """
        return float(self.value)

    def __getitem__(self, item: int) -> float:
        """ Get the mean value or the confidence interval.

        :param item: 0 for the mean value, 1 for the confidence interval.
        :return: The float value of the mean value or the confidence interval.
        """
        return tuple(self)[item]

    def __cmp__(self, other: Any) -> float:
        """ Compare two values.

        :param other: The other value with confidence intervals.
        :return: this value minus the other value.
        """
        return self.value - float(other)

    def __hash__(self) -> int:
        """ A hash representation of this confidence interval. """
        return hash((self.value, self.ci))

    def __contains__(self, other: 'CI') -> bool:
        """ If this confidence interval contains other one.

        :param other: The other value with confidence intervals.
        :return: True if this confidence interval contains the other one.
        """
        return other.min >= self.min and other.max <= self.max

    def __copy__(self) -> 'CI':
        return CI(self.value, self.ci, self.p)

    def __pow__(self, power, **kwargs) -> float:
        return None if self.p is None else self.p ** power

    def __complex__(self) -> complex:
        return complex(self.value, self.ci)
