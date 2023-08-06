from enum import Enum, unique
from math import ceil, floor
from typing import Generic, TypeVar, Union, List, Iterable, Any
import sklearn.metrics

from myskutils.ci import CI

T = TypeVar('T')


# MEASURES ATTRIBUTES
@unique
class MetricName(Enum):
    SIMPLE_ACCURACY = 'accuracy'
    BALANCED_ACCURACY = 'balanced_accuracy'
    MICRO_F1 = 'micro_f1'
    MACRO_F1 = 'macro_f1'
    WEIGHTED_F1 = 'weighted_f1'
    MICRO_PRECISION = 'micro_precision'
    MACRO_PRECISION = 'macro_precision'
    WEIGHTED_PRECISION = 'weighted_precision'
    MICRO_RECALL = 'micro_recall'
    MACRO_RECALL = 'macro_recall'
    WEIGHTED_RECALL = 'weighted_recall'
    MICRO_JACCARD = 'micro_jaccard'
    MACRO_JACCARD = 'macro_jaccard'
    WEIGHTED_JACCARD = 'weighted_jaccard'

    def calculate(self, trues: List[float], predictions: List[float]) -> 'Metric':
        func_name = self.value
        if 'micro' in func_name:
            average = 'micro'
        elif 'macro' in func_name:
            average = 'macro'
        elif 'weighted' in func_name:
            average = 'weighted'
        else:
            average = None
        func_name = func_name[len(average) + 1:] + '_score' if average else func_name + '_score'
        func = getattr(sklearn.metrics, func_name)
        return Metric(self.value, func(trues, predictions, **({'average': average} if average else {})))

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: Union['MetricName', str]) -> bool:
        return self.value == other if isinstance(other, str) else self.value == other.value and self.name == other.name

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def contains(value: Any) -> bool:
        return str(value).lower() in {str(metric).lower() for metric in MetricName}


class Metric(Generic[T]):
    @property
    def name(self) -> MetricName:
        return self.__name

    @property
    def value(self) -> T:
        return self.__value

    def __init__(self, name: Union[MetricName, str], value: T) -> None:
        self.__name = name
        if isinstance(value, tuple) and 2 <= len(value) <= 3:
            self.__value = CI(value[0], value[1]) if len(value) == 2 else CI(value[0], value[1], value[3])
        else:
            self.__value = value

    def less_uncertainty(self, other: 'Metric[CI]') -> bool:
        return other is None or self.value.max - self.value.min < other.value.max - other.value.min

    def greater_uncertainty(self, other: 'Metric[CI]') -> bool:
        return other is None or self.value.max - self.value.min > other.value.max - other.value.min

    def in_interval(self, measures: Iterable['Metric[CI]']) -> List['Metric[CI]']:
        return [measure for measure in measures if not self.value.is_significant(measure.value)]

    @staticmethod
    def max_min_interval(measures: List['Metric[CI]']) -> 'Metric[CI]':
        return max(measures, key=lambda x: x.value - x.min)

    @staticmethod
    def min_max_interval(measures: List['Metric[CI]']) -> 'Metric[CI]':
        return min(measures, key=lambda x: x.value + x.max)

    def has_confidence(self) -> bool:
        return isinstance(self.__value, CI)

    def format(self, precision: int = 2) -> str:
        """
        Format the metrics.
        :param precision: The number of decimal places.
        :return: The formatted value.
        """
        pattern = f'{{0:.{precision}f}}'
        if isinstance(self.value, float):
            return pattern.format(self.value * 100)
        return pattern.format(self.value.value * 100) + '±' + pattern.format(self.value.ci * 100)

    @staticmethod
    def from_dict(d: dict) -> List['Metric']:
        return [Metric(name, value) for name, value in d.items()]

    def to_data(self) -> Union[float, tuple]:
        value = self.__value
        if isinstance(value, CI):
            return (value.value, value.ci, value.p) if value.p is None else (value.value, self.value.ci)

    def __len__(self) -> int:
        return 2

    def __iter__(self) -> Iterable:
        return iter((self.name, self.value))

    def __str__(self) -> str:
        return f'{self.name}={str(self.__value)}'

    def __repr__(self) -> str:
        return f'Metric({repr(self.__name)}, {repr(self.__value)})'

    def __eq__(self, other: Any) -> bool:
        if other is None:
            raise ValueError('It is not possible to compare with None value.')
        return self.__value == str(other)

    def __ne__(self, other: Any) -> bool:
        if other is None:
            raise ValueError('It is not possible to compare with None value.')
        return not self == str(other)

    def __gt__(self, other: Any) -> bool:
        if other is None:
            raise ValueError('It is not possible to compare with None value.')
        return self.__value > str(other)

    def __lt__(self, other: Any) -> bool:
        if other is None:
            raise ValueError('It is not possible to compare with None value.')
        return self.__value < str(other)

    def __ge__(self, other: Any) -> bool:
        if other is None:
            raise ValueError('It is not possible to compare with None value.')
        return self.__value >= other.__value

    def __le__(self, other: Any) -> bool:
        if other is None:
            raise ValueError('It is not possible to compare with None value.')
        return self.__value <= other.__value

    def __hash__(self) -> int:
        return hash(self.__name)

    def __pow__(self, power: float, **kwargs) -> 'Metric':
        return Metric(self.__name, self.__value ** power)

    def __sum__(self, other: Union['Metric', int, float]) -> 'Metric':
        if isinstance(other, Metric) and self.__name != other.__name:
            raise ValueError('To sum two measures it is necessary to have the same name.')
        return Metric(self.__name, self.__value ** (other.__value if isinstance(other, Metric) else other))

    def __sub__(self, other: Union['Metric', int, float]) -> 'Metric':
        if isinstance(other, Metric) and self.__name != other.__name:
            raise ValueError('To sum two measures it is necessary to have the same name.')
        return Metric(self.__name, self.__value ** (other.__value if isinstance(other, Metric) else other))

    def __mul__(self, other: Union['Metric', int, float]) -> 'Metric':
        if isinstance(other, Metric) and self.__name != other.__name:
            raise ValueError('To sum two measures it is necessary to have the same name.')
        return Metric(self.__name, self.__value * (other.__value if isinstance(other, Metric) else other))

    def __divmod__(self, num: int) -> 'Metric':
        if not isinstance(num, int):
            raise ValueError('The entire division requires a integer number.')
        return Metric(self.__name, self.__value // num)

    def __mod__(self, num: int) -> 'Metric':
        if not isinstance(num, int):
            raise ValueError('The calculate the module requires a integer number.')
        return Metric(self.__name, self.__value % num)

    def __bool__(self) -> bool:
        return bool(self.__value)

    def __float__(self) -> float:
        return float(self.__value)

    def __ceil__(self) -> 'Metric':
        return Metric(self.__name, ceil(self.__value))

    def __floor__(self) -> 'Metric':
        return Metric(self.__name, floor(self.__value))

    def __int__(self) -> int:
        return int(self.__value)
