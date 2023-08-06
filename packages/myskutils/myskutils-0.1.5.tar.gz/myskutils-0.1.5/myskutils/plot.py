from typing import List, Union, Dict, Tuple, Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from mysutils.collections import merge_tuples

from myskutils.measure import Metric, CI


def plot_measures(measures: List[Union[float, Tuple[float, float]]],
                  xticks: Iterable[str],
                  filename: str = None,
                  color: str = 'black',
                  capsize: int = 3,
                  linestyle: str = 'None',
                  marker: str = 's',
                  markersize: int = 7,
                  mfc: str = 'black',
                  mec: str = 'black',
                  **kwargs) -> None:
    d = {name: measures[i] for i, name in enumerate(xticks)}
    plot_measure(d, xticks, filename, color, capsize, linestyle, marker, markersize, mfc, mec, **kwargs)


def plot_measure(measure: Dict[str, Union[float, Tuple[float, float]]],
                 detail: bool = True,
                 xticks: Iterable[str] = None,
                 filename: str = None,
                 color: str = 'black',
                 capsize: int = 3,
                 linestyle: str = 'None',
                 marker: str = 's',
                 markersize: int = 7,
                 mfc: str = 'black',
                 mec: str = 'black',
                 **kwargs) -> None:
    x = np.arange(1, len(measure) + 1)
    plt.figure(figsize=(8, 7))
    plt.xticks(x, xticks if xticks else measure, rotation=90)
    if not detail:
        plt.ylim(ymin=0)
    if measure.values() and isinstance(list(measure.values())[0], tuple):
        y, err = merge_tuples(measure.values())
        plt.errorbar(x=x, y=y, yerr=err, color=color, capsize=capsize, linestyle=linestyle, marker=marker,
                     markersize=markersize, mfc=mfc, mec=mec, **kwargs)
    else:
        plt.bar(x=x, height=measure.values(), color=color, capsize=capsize, linestyle=linestyle, **kwargs)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()


def plot(measures: List[Metric],
         detail: bool = True,
         xticks: Iterable[str] = None,
         filename: str = None,
         color: str = 'black',
         capsize: int = 3,
         linestyle: str = 'None',
         marker: str = 's',
         markersize: int = 7,
         mfc: str = 'black',
         mec: str = 'black',
         **kwargs) -> None:
    x = np.arange(1, len(measures) + 1)
    plt.figure(figsize=(8, 7))
    plt.xticks(x, xticks if xticks else [m.name for m in measures], rotation=90)
    if not detail:
        plt.ylim(ymin=0)
    if measures and isinstance(measures[0].value, CI):
        y, err = merge_tuples([(m.value.value, m.value.ci) for m in measures])
        plt.errorbar(x=x, y=y, yerr=err, color=color, capsize=capsize, linestyle=linestyle, marker=marker,
                     markersize=markersize, mfc=mfc, mec=mec, **kwargs)
    else:
        plt.bar(x=x, height=[m.value for m in measures], color=color, capsize=capsize, linestyle=linestyle, **kwargs)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()


def get_graph_data(data: dict) -> Tuple[dict, dict, list]:
    graph_data = {}
    err = {}
    labels = []
    for corpus_name, metrics in data.items():
        graph_data[corpus_name], err[corpus_name] = {}, {}
        for i, (metric, value) in enumerate(metrics.items()):
            if i < len(labels):
                if labels[i] != metric:
                    raise ValueError('To generate a figure with different corpus,'
                                     ' it is necessary that they have the same metrics in the same order.')
            else:
                labels.append(metric)
            if metric not in err[corpus_name]:
                err[corpus_name][metric] = [[], []]
            graph_data[corpus_name][metric] = value[0]

            err[corpus_name][metric][0].append(value[1])
            err[corpus_name][metric][1].append(value[1])
    return graph_data, err, labels


def plot_figure(data: dict, bar_width: float = 0.8) -> Figure:
    graph_data, err, labels = get_graph_data(data)
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(labels))
    width = bar_width / len(data)
    for i, corpus in enumerate(data):
        values = [v for v in graph_data[corpus].values()]
        errs = [v[0][0] for v in err[corpus].values()]
        ax.barh(x - width * i + width/2, values, width, xerr=errs, capsize=3, label=corpus)
    ax.invert_yaxis()
    ax.set_yticks(x, labels=labels)
    ax.legend(loc=(1, 0.05))
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_facecolor((1.0, 1.0, 1.0))
    fig.patch.set_facecolor('white')
    fig.tight_layout()
    return fig
