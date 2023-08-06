from typing import List, Dict, Tuple, Union, Optional, Iterable

import numpy as np
import scipy.stats as st
from mysutils.collections import merge_dicts, merge_tuples


def confidence_score(measures: Union[Iterable[Dict[str, float]], Dict[str, List[float]]],
                     ci: float = 0.95) -> Dict[str, Tuple[float, float]]:
    """ Obtain the mean value and confidence interval for a list of measures for different metrics.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :param ci: The coefficient interval threshold in a value between 0 and 1.
    :return: A dictionary with the different metrics and a tuple with the mean value and the confidence interval.
    """
    measures = merge_dicts(measures) if isinstance(measures, List) else measures
    intervals = {key: st.t.interval(ci, len(v) - 1, loc=np.mean(v), scale=st.sem(v)) for key, v in measures.items()}
    return {key: ((b + a) / 2, (b - a) / 2) for key, (a, b) in intervals.items()}


def measures_mean(measures: Iterable[Dict[str, float]]) -> Dict[str, float]:
    """ Obtain the mean value of a list of measures for different metrics without confidence interval.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :return: A dictionary with the different metrics and the mean value of each metric.
    """
    measures = merge_dicts(measures) if isinstance(measures, Iterable) else measures
    return {key: np.mean(values) for key, values in measures.items()}


def confidence_mean(measures: Union[Iterable[Dict[str, tuple]], Dict[str, List[tuple]]]) -> Dict[str, tuple]:
    """ Obtain the mean value of a list of measures for different metrics with confidence interval.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :return: A dictionary with the different metrics and the mean value of each metric.
    """
    measures = merge_dicts(measures) if isinstance(measures, Iterable) else measures
    return {key: (np.mean(merge_tuples(val)[0]), np.mean(merge_tuples(val)[1])) for key, val in measures.items()}


def standard_deviation(measures: Union[Iterable[Dict[str, float]], Dict[str, List[float]]]) -> Dict[str, float]:
    """ Obtain the standard deviation of a list of measures for different metrics.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :return: A dictionary with the different metrics and the standard deviation of each metric.
    """
    measures = merge_dicts(measures) if isinstance(measures, Iterable) else measures
    return {key: np.std(values) for key, values in measures.items()}


def standard_error(measures: Union[Iterable[Dict[str, float]], Dict[str, List[float]]]) -> Dict[str, float]:
    """ Obtain the standard error of a list of measures for different metrics.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :return: A dictionary with the different metrics and the standard error of each metric.
    """
    measures = merge_dicts(measures) if isinstance(measures, Iterable) else measures
    return {key: np.std(values) / len(values) for key, values in measures.items()}


def min_uncertainty(measures: Iterable[Dict[str, Tuple[float, float]]]) -> Tuple[str, Tuple[float, float]]:
    """ Obtain the key of the value with minimum uncertainty.

    :param measures: A measure dictionary with the different metrics or a list of measures.
    :return: A tuple with the key of the value with minimum uncertainty, and a tuple with the value and the confidence.
    """
    mean = confidence_mean(measures)
    return min(mean.items(), key=lambda x: x[1][1])


def max_uncertainty(measures: Iterable[Dict[str, Tuple[float, float]]]) -> Tuple[str, Tuple[float, float]]:
    """ Obtain the key of the value with minimum uncertainty.

    :param measures: A measure dictionary with the different metrics or a list of measures.
    :return: A tuple with the key of the value with minimum uncertainty, and a tuple with the value and the confidence.
    """
    mean = confidence_mean(measures)
    return max(mean.items(), key=lambda x: x[1][1])


def min_value(measures: Iterable[Dict[str, Tuple[float, float]]]) -> Union[Tuple[str, Tuple[float, float]], list]:
    """ Obtain the key of the value with minimum uncertainty.

    :param measures: A measure dictionary with the different metrics or a list of measures.
    :return: A tuple with the key of the value with minimum uncertainty, and a tuple with the value and the confidence.
    """
    if has_confidence(measures):
        mean = confidence_mean(measures)
        min_max = min_max_interval(mean)
        return sorted(in_interval(min_max[1]), key=lambda x: x[1])
    else:
        mean = measures_mean(measures)
        return min(mean.items(), key=lambda x: x[1])


def max_value(measures: Iterable[Dict[str, Tuple[float, float]]]) -> Union[Tuple[str, Tuple[float, float]], list]:
    """ Obtain the key of the value with minimum uncertainty.

    :param measures: A measure dictionary with the different metrics or a list of measures.
    :return: A tuple with the key of the value with minimum uncertainty, and a tuple with the value and the confidence.
    """
    if has_confidence(measures):
        mean = confidence_mean(measures)
        max_min = max_min_interval(mean)
        return sorted(in_interval(max_min[1], mean), key=lambda x: -x[1])
    else:
        mean = measures_mean(measures)
        return max(mean.items(), key=lambda x: x[1])


def max_min_interval(measures: Dict[str, Tuple[float, float]]) -> Tuple[str, Tuple[float, float]]:
    return max(measures.items(), key=lambda x: x[1][0] - x[1][1])


def min_max_interval(measures: Dict[str, Tuple[float, float]]) -> Tuple[str, Tuple[float, float]]:
    return min(measures.items(), key=lambda x: x[1][0] + x[1][1])


def in_interval(interval: Tuple[float, float], measures: Dict[str, Tuple[float, float]]) -> List[Tuple[str, float, float]]:
    return [(metric, value, conf) for metric, (value, conf) in measures.items() if not is_significant(interval, (value, conf))]


def intervals_in_max_value(measures):
    results = []
    for key, (value, conf) in sorted(measures.items(), key=lambda x: -x[1][0]):
        if not results or not is_significant((value, conf), (results[0][1], results[0][2])):
            results.append((key, value, conf))
    return results


def is_significant(value1: Tuple[float, float], value2: Tuple[float, float]) -> bool:
    return value1[0] + value1[1] < value2[0] - value2[1] or value1[0] - value1[1] > value2[0] + value2[1]


def has_confidence(measures: Union[Dict[str, Tuple[float, float]],
                                   Iterable[Dict[str, Tuple[float, float]]]]) -> Optional[bool]:
    """ Check if a dictionary with a list of values has confidence interval.

    :param measures: The dictionary in which each element contains a list of values. If this values are all
    :return: True if the values are list of tuples with two float values, False otherwise.
    """
    measures = [measures] if isinstance(measures, dict) else measures
    for measure in measures:
        for v in measure.values():
            if not isinstance(v, tuple) or len(v) != 2 or not isinstance(v[0], float) or not isinstance(v[1], float):
                return False
    return True
