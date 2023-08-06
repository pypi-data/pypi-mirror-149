from json import JSONEncoder
from sys import stdout
from typing import Generic, Union, List, Iterable, Dict, TextIO, ItemsView, Any
from statistics import mean, stdev
from mysutils.collections import merge_dicts
from mysutils.file import open_file

from myskutils.ci import CI
from myskutils.metric import T, Metric, MetricName


def filter_measure(data: dict, *metrics):
    return {k: v for k, v in data.items() if k in metrics}


class Measure(Generic[T], JSONEncoder):
    @property
    def metrics(self) -> Iterable[Metric]:
        return self.__metrics.values()

    @staticmethod
    def metric_names() -> List[str]:
        return [metric.value for metric in MetricName]

    def __init__(self, *metrics: Metric) -> None:
        self.__metrics = {metric.name: metric for metric in metrics}

    @staticmethod
    def from_evaluation(trues: List[float], predictions: List[float], *select: Union[MetricName, str]) -> 'Measure':
        select = select if select else (metric for metric in MetricName)
        return Measure(*[metric.calculate(trues, predictions) for metric in select])

    @staticmethod
    def from_dict(d: dict) -> 'Measure':
        return Measure(*[Metric(name, value) for name, value in d.items()])

    def select(self, *metric_names: Union[MetricName, str]) -> 'Measure':
        return Measure(*[self.__metrics[metric] for metric in metric_names])

    def value(self, metric: Union[MetricName, str]) -> T:
        return self.__metrics[metric].value

    def items(self) -> ItemsView[str, T]:
        return {k: v.value for k, v in self.__metrics.items()}.items()

    @staticmethod
    def values(measures: List['Measure'], metric: Union[MetricName, str]) -> List[T]:
        return [measure.value(metric) for measure in measures]

    @staticmethod
    def confidence_score(measures: List['Measure'], alpha: float = 0.95) -> 'Measure':
        d = {name: CI.confidence_score(lst, alpha) for name, lst in merge_dicts(measures).items()}
        return Measure.from_dict(d)

    @staticmethod
    def confidence_score_from_dict(d: Dict[str, List[float]], alpha: float = 0.95) -> 'Measure':
        """ Create a measure with confidence interval from a list with the follow syntax:

        .. code-block::

            d = {
                'Metric_name1': [v1.1, v1.2, v1.3, ..., v1.n],
                'Metric_name2': [v2.1, v2.2, v2.3, ..., v2.n],
                ...
                'Metric_nameM': [vM.1, vM.2, vM.3, ..., vM.n],
            }

        Where *Metric_nameX* is the metric name, and *vX.Y* is the different values of each metric.

        :param d: The dictionary with the metrics names and the list of values.
        :param alpha: The alpha value for the confidence interval. An alpha of 0.95 is a p value < 0.05.
        :return: A measure object with mean value and confidence interval for all the metrics in the dictionary.
        """
        d = {name: CI.confidence_score(lst, alpha) for name, lst in d.items()}
        return Measure.from_dict(d)

    @staticmethod
    def mean(measures: List['Measure']) -> 'Measure':
        d = {name: mean(lst) for name, lst in merge_dicts(measures).items()}
        return Measure.from_dict(d)

    @staticmethod
    def std(measures: Iterable['Measure']) -> 'Measure':
        d = {name: stdev(lst) for name, lst in merge_dicts(measures).items()}
        return Measure.from_dict(d)

    @staticmethod
    def standard_error(measures: List['Measure']) -> 'Measure':
        d = {name: stdev(lst) / len(measures) for name, lst in merge_dicts(measures).items()}
        return Measure.from_dict(d)

    def metric(self, name: [MetricName, str], new_name: str = None) -> Metric[T]:
        return Metric(new_name if new_name else name, self.__metrics[name].value)

    def print(self, *metrics: Union[MetricName, str], output: Union[TextIO, str] = stdout) -> None:
        """ Print a measure with different metrics.
        :param metrics: The list to measures to print.
        :param output: The file handler or the file path where the result are printed.
           By default in the standard output.
        """
        metrics = metrics if metrics else {(str(metric)) for metric in self.metrics}
        file = open_file(output, 'wt') if isinstance(output, str) else output
        # if str(MetricName.SIMPLE_ACCURACY).lower() in metrics or MetricName.BALANCED_ACCURACY in metrics:
        #     self._print_metric_if_show('Simple accuracy', MetricName.SIMPLE_ACCURACY, *metrics, file=file)
        #     self._print_metric_if_show('Balanced accuracy', MetricName.BALANCED_ACCURACY, *metrics, file=file)
        #     print(file=file)
        # if MetricName.MICRO_F1 in metrics or MetricName.MACRO_F1 in metrics or MetricName.WEIGHTED_F1 in metrics:
        #     self._print_metric_if_show('Micro f-measure', MetricName.MICRO_F1, *metrics, file=file)
        #     self._print_metric_if_show('Macro f-measure', MetricName.MACRO_F1, *metrics, file=file)
        #     self._print_metric_if_show('Weighted f-measure', MetricName.WEIGHTED_F1, *metrics, file=file)
        #     print(file=file)
        # if MetricName.MICRO_PRECISION in metrics or\
        #         MetricName.MACRO_PRECISION in metrics or\
        #         MetricName.WEIGHTED_PRECISION in metrics:
        #     self._print_metric_if_show('Micro precision', MetricName.MICRO_PRECISION, *metrics, file=file)
        #     self._print_metric_if_show('Macro precision', MetricName.MACRO_PRECISION, *metrics, file=file)
        #     self._print_metric_if_show('Weighted precision', MetricName.WEIGHTED_PRECISION, *metrics, file=file)
        #     print(file=file)
        # if MetricName.MICRO_RECALL in metrics or\
        #         MetricName.MACRO_RECALL in metrics or\
        #         MetricName.WEIGHTED_RECALL in metrics:
        #     self._print_metric_if_show('Micro recall', MetricName.MICRO_RECALL, *metrics, file=file)
        #     self._print_metric_if_show('Macro recall', MetricName.MACRO_RECALL, *metrics, file=file)
        #     self._print_metric_if_show('Weighted recall', MetricName.WEIGHTED_RECALL, *metrics, file=file)
        #     print(file=file)
        # if MetricName.MICRO_JACCARD in metrics or\
        #         MetricName.MACRO_JACCARD in metrics or\
        #         MetricName.WEIGHTED_JACCARD in metrics:
        #     self._print_metric_if_show('Micro Jaccard', MetricName.MICRO_JACCARD, *metrics, file=file)
        #     self._print_metric_if_show('Macro Jaccard', MetricName.MACRO_JACCARD, *metrics, file=file)
        #     self._print_metric_if_show('Weighted Jaccard', MetricName.WEIGHTED_JACCARD, *metrics, file=file)
        #     print(file=file)
        for i, metric in enumerate(metrics):
            if i % 3 == 0:
                print(file=file)
            print(f'{metric}: ', self[metric].format(), end='\t', file=file)
        if isinstance(output, str):
            file.close()

    # def _print_metric_if_show(self, msg: str, metric: MetricName, *show: MetricName, file: TextIO):
    #     """ Print a given metric if that metric is selected.
    #     :param msg: The message to print with the metric.
    #     :param metrics: All obtained metrics.
    #     :param metric: The metric to print.
    #     :param show: The list of metrics which will be printed.
    #     :param file: The file handler where the result are printed. By default in the standard output.
    #     """
    #     if metric in show:
    #         print(f'{msg}: ', self[metric].format(), end='\t', file=file)

    def min_uncertainty(self) -> Metric:
        min_ci = None
        for metric in self.__metrics.values():
            min_ci = metric if metric.less_uncertainty(min_ci) else min_ci
        return min_ci

    def max_uncertainty(self) -> Metric:
        max_ci = None
        for metric in self.__metrics.values():
            max_ci = metric if metric.greater_uncertainty(max_ci) else max_ci
        return max_ci

    def min_value(self) -> Metric:
        min_v = None
        for metric in self.__metrics.values():
            min_v = metric if metric < min_v else min_v
        return min_v

    def max_value(self) -> Metric:
        max_v = None
        for metric in self.__metrics.values():
            max_v = metric if metric > max_v else max_v
        return max_v

    def __getitem__(self, item: Union[str, MetricName]):
        return self.__metrics[item]

    def __iter__(self) -> Iterable[Metric]:
        return iter({metric.name: tuple(metric.value) if isinstance(metric.value, CI) else metric.value
                     for metric in self.metrics}.items())

    def __str__(self) -> str:
        return 'Measure(' + ', '.join([str(metric) for metric in self.__metrics.values()]) + ')'

    def __repr__(self) -> str:
        return 'Measure(' + ', '.join([repr(metric) for metric in self.__metrics.values()]) + ')'

