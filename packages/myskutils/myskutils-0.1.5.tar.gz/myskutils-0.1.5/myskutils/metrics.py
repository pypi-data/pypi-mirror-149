from sys import stdout
from typing import List, Dict, TextIO, Tuple, Union

from mysutils.file import open_file
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score, \
    jaccard_score

# MEASURES ATTRIBUTES
SIMPLE_ACCURACY = 'simple_accuracy'
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
ALL_METRICS = (SIMPLE_ACCURACY, BALANCED_ACCURACY, MICRO_F1, MACRO_F1, WEIGHTED_F1, MICRO_PRECISION, MACRO_PRECISION,
               WEIGHTED_PRECISION, MICRO_RECALL, MACRO_RECALL, WEIGHTED_RECALL, MICRO_JACCARD, MACRO_JACCARD,
               WEIGHTED_JACCARD)


def sk_measure(trues: List[int], predictions: List[int]) -> Dict[str, float]:
    """ Measure with different sklearn metrics from the list of real classes and the predicted ones.
    :param trues: The real classes for each sample.
    :param predictions: The predicted classes for each sample.
    :return: A dictionary with the measure names and their respective values.
    """
    met = {SIMPLE_ACCURACY: accuracy_score(trues, predictions),
           BALANCED_ACCURACY: balanced_accuracy_score(trues, predictions),
           MICRO_F1: f1_score(trues, predictions, average='micro'),
           MACRO_F1: f1_score(trues, predictions, average='macro'),
           WEIGHTED_F1: f1_score(trues, predictions, average='weighted'),
           MICRO_PRECISION: precision_score(trues, predictions, average='micro'),
           MACRO_PRECISION: precision_score(trues, predictions, average='macro'),
           WEIGHTED_PRECISION: precision_score(trues, predictions, average='weighted'),
           MICRO_RECALL: recall_score(trues, predictions, average='micro'),
           MACRO_RECALL: recall_score(trues, predictions, average='macro'),
           WEIGHTED_RECALL: recall_score(trues, predictions, average='weighted'),
           MICRO_JACCARD: jaccard_score(trues, predictions, average='micro'),
           MACRO_JACCARD: jaccard_score(trues, predictions, average='macro'),
           WEIGHTED_JACCARD: jaccard_score(trues, predictions, average='weighted')}
    return met


def print_metrics(measure: Dict[str, Union[float, Tuple[float, float]]],
                  metrics: List[str] = ALL_METRICS,
                  output: Union[TextIO, str] = stdout) -> None:
    """ Print a measure with different metrics.
    :param measure: The a dictionary with the metrics to print.
    :param metrics: The list to measures to print.
    :param output: The file handler or the file path where the result are printed.
       By default in the standard output.
    """
    file = open_file(output, 'wt') if isinstance(output, str) else output
    _print_metric_if_show('Simple accuracy', measure, SIMPLE_ACCURACY, metrics, file)
    _print_metric_if_show('Balanced accuracy', measure, BALANCED_ACCURACY, metrics, file)
    print(file=file)
    _print_metric_if_show('Micro f-measure', measure, MICRO_F1, metrics, file)
    _print_metric_if_show('Macro f-measure', measure, MACRO_F1, metrics, file)
    _print_metric_if_show('Weighted f-measure', measure, WEIGHTED_F1, metrics, file)
    print(file=file)
    _print_metric_if_show('Micro precision', measure, MICRO_PRECISION, metrics, file)
    _print_metric_if_show('Macro precision', measure, MACRO_PRECISION, metrics, file)
    _print_metric_if_show('Weighted precision', measure, WEIGHTED_PRECISION, metrics, file)
    print(file=file)
    _print_metric_if_show('Micro recall', measure, MICRO_RECALL, metrics, file)
    _print_metric_if_show('Macro recall', measure, MACRO_RECALL, metrics, file)
    _print_metric_if_show('Weighted recall', measure, WEIGHTED_RECALL, metrics, file)
    print(file=file)
    _print_metric_if_show('Micro Jaccard', measure, MICRO_JACCARD, metrics, file)
    _print_metric_if_show('Macro Jaccard', measure, MACRO_JACCARD, metrics, file)
    _print_metric_if_show('Weighted Jaccard', measure, WEIGHTED_JACCARD, metrics, file)
    print(file=file)
    if isinstance(output, str):
        file.close()


def select_metrics(measure: Dict[str, Union[float, Tuple[float, float]]],
                   *metrics: str) -> Dict[str, Union[float, Tuple[float, float]]]:
    """ From all the metrics of a given measure, select only the defined ones.

    :param measure: The measure with different metrics.
    :param metrics: The metric names to select.
    :return: A dictionary with the names of the selected metrics and their values.
    """
    return {key: value for key, value in measure.items() if key in metrics}


def _print_metric_if_show(msg: str, metrics: Dict[str, Union[float, Tuple[float, float]]],
                          metric: str, show: List[str], file: TextIO):
    """ Print a given metric if that metric is selected.
    :param msg: The message to print with the metric.
    :param metrics: All obtained metrics.
    :param metric: The metric to print.
    :param show: The list of metrics which will be printed.
    :param file: The file handler where the result are printed. By default in the standard output.
    """
    if metric in show:
        print(f'{msg}: ', format_value(metrics[metric]), end='\t', file=file)


def format_value(value: Union[float, Tuple[float, float]], precision: int = 2) -> str:
    """
    Format the metrics.
    :param value: The value to format.
    :param precision: The number of decimal places.
    :return: The formatted value.
    """
    pattern = f'{{0:.{precision}f}}'
    if isinstance(value, float):
        return pattern.format(value * 100)
    return pattern.format(value[0] * 100) + '±' + pattern.format(value[1] * 100)
