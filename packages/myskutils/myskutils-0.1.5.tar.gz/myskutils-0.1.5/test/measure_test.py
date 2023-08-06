import unittest

from mysutils.file import load_json

from myskutils.measure import Measure, MetricName, CI, Metric
from myskutils.plot import plot, plot_figure
from test.results import conf_99

Y_TRUES_FILE = 'test/trues.json'
Y_PRED_FILE = 'test/pred.json'
MEASURES_FILE = 'test/data.json'
CONF_95_FILE = 'test/conf_95.json'
CONF_99_FILE = 'test/conf_99.json'
result = {
    'accuracy': 0.7314814814814815, 'balanced_accuracy': 0.7336080586080586,
    'micro_f1': 0.7314814814814816, 'macro_f1': 0.6676911015978718, 'weighted_f1': 0.7064382543140714,
    'micro_precision': 0.7314814814814815, 'macro_precision': 0.6733602875112309,
    'weighted_precision': 0.7421737213403881, 'micro_recall': 0.7314814814814815,
    'macro_recall': 0.7197663971248877, 'weighted_recall': 0.7314814814814815,
    'micro_jaccard': 0.5766423357664233, 'macro_jaccard': 0.6027144762993819,
    'weighted_jaccard': 0.6215661910106355
}


class MyTestCase(unittest.TestCase):
    def test_format_values(self) -> None:
        y_trues, y_pred = load_json(Y_TRUES_FILE), load_json(Y_PRED_FILE)
        measure = Measure.from_evaluation(y_trues, y_pred)
        # self.assertDictEqual(result, measure.to_dict())  # add assertion here
        self.assertEqual(measure[MetricName.SIMPLE_ACCURACY].format(), '73.15')
        self.assertEqual(measure[MetricName.SIMPLE_ACCURACY].format(3), '73.148')
        self.assertEqual(measure[MetricName.SIMPLE_ACCURACY].format(0), '73')

    def test_print(self):
        measure = Measure.from_evaluation(load_json(Y_TRUES_FILE), load_json(Y_PRED_FILE))
        measure.print()
        measure.select('accuracy').print()
        self.assertEqual(True, True)  # add assertion here

    def test_confidence_interval(self) -> None:
        measures = [Measure.from_dict(eval) for eval in load_json(MEASURES_FILE)]

        ci_measures = Measure.confidence_score(measures, 0.95)
        self.assertEqual(str(ci_measures.select(MetricName.WEIGHTED_F1)),
                         'Measure(weighted_f1=0.6897580626192598±0.03565990800863161)')
        self.assertEqual(str(ci_measures.metric(MetricName.WEIGHTED_F1, 'BERT_MODEL')),
                         'BERT_MODEL=0.6897580626192598±0.03565990800863161')
        self.assertEqual(str(ci_measures.min_uncertainty()), 'balanced_accuracy=0.695702864876455±0.0315404522111038')
        self.assertEqual(str(ci_measures.max_uncertainty()), 'micro_jaccard=0.5316665991417848±0.040809554891851146')
        self.assertEqual(str(ci_measures.min_value()), 'micro_jaccard=0.5316665991417848±0.040809554891851146')
        self.assertEqual(str(ci_measures.max_value()), 'weighted_precision=0.7389542915931806±0.03589302220107715')
        self.assertEqual(str(ci_measures.min_value().in_interval(ci_measures.metrics)),
                         '[micro_jaccard=0.5316665991417848±0.040809554891851146, '
                         'macro_jaccard=0.5584330739064476±0.03740462144237966, '
                         'weighted_jaccard=0.602431880785639±0.035765269919655784]')
        self.assertEqual(str(ci_measures.max_value().in_interval(ci_measures.metrics)),
                         '[simple_accuracy=0.6925925925925926±0.03502136605451667, '
                         'balanced_accuracy=0.695702864876455±0.0315404522111038, '
                         'micro_f1=0.6925925925925926±0.03502136605451667, '
                         'weighted_f1=0.6897580626192598±0.03565990800863161, '
                         'micro_precision=0.6925925925925926±0.03502136605451667, '
                         'weighted_precision=0.7389542915931806±0.03589302220107715, '
                         'micro_recall=0.6925925925925926±0.03502136605451667, '
                         'weighted_recall=0.6925925925925926±0.03502136605451667]')
        plot(list(ci_measures.metrics))

    def test_plot(self) -> None:
        fig = plot_figure(conf_99)
        fig.show()

    def test_measures(self) -> None:
        ci1, ci2, ci3 = CI(0.51, 0.12), CI(0.72, 0.25), CI(0.81, 0.09)

        measure = Measure(Metric('Accuracy', ci1), Metric('F1-score', ci2), Metric('Precision', ci3))
        self.assertDictEqual(dict(measure), {'Accuracy': (0.51, 0.12),
                                             'F1-score': (0.72, 0.25),
                                             'Precision': (0.81, 0.09)})

        measure = Measure(Metric(MetricName.SIMPLE_ACCURACY, ci1),
                          Metric(MetricName.WEIGHTED_F1, ci2),
                          Metric(MetricName.MACRO_PRECISION, ci3))
        self.assertDictEqual(dict(measure), {'accuracy': (0.51, 0.12),
                                             'weighted_f1': (0.72, 0.25),
                                             'macro_precision': (0.81, 0.09)})
        pass


if __name__ == '__main__':
    unittest.main()
