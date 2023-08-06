import unittest


from myskutils.measure import CI
from test.results import conf_95, conf_6_3_99, mean, sd, se

from mysutils.file import load_json

from myskutils.metrics import sk_measure, SIMPLE_ACCURACY, format_value, select_metrics, MACRO_JACCARD, MACRO_F1, \
    MACRO_RECALL
from myskutils.stats import confidence_score, measures_mean, standard_deviation, standard_error, min_uncertainty, \
    has_confidence, max_uncertainty, min_value, max_value
from myskutils.plot import plot_measure

Y_TRUES_FILE = 'test/trues.json'
Y_PRED_FILE = 'test/pred.json'
MEASURES_FILE = 'test/data.json'
CONF_95_FILE = 'test/conf_95.json'
CONF_99_FILE = 'test/conf_99.json'
result = {
    'simple_accuracy': 0.7314814814814815, 'balanced_accuracy': 0.7336080586080586,
    'micro_f1': 0.7314814814814816, 'macro_f1': 0.6676911015978718, 'weighted_f1': 0.7064382543140714,
    'micro_precision': 0.7314814814814815, 'macro_precision': 0.6733602875112309,
    'weighted_precision': 0.7421737213403881, 'micro_recall': 0.7314814814814815,
    'macro_recall': 0.7197663971248877, 'weighted_recall': 0.7314814814814815,
    'micro_jaccard': 0.5766423357664233, 'macro_jaccard': 0.6027144762993819,
    'weighted_jaccard': 0.6215661910106355
}


class MyTestCase(unittest.TestCase):
    def test_measurement(self) -> None:
        y_trues, y_pred = load_json(Y_TRUES_FILE), load_json(Y_PRED_FILE)
        measure = sk_measure(y_trues, y_pred)
        self.assertDictEqual(result, measure)  # add assertion here
        self.assertEqual(format_value(measure[SIMPLE_ACCURACY]), '73.15')
        self.assertEqual(format_value(measure[SIMPLE_ACCURACY], 3), '73.148')
        self.assertEqual(format_value(measure[SIMPLE_ACCURACY], 0), '73')

    def test_list_measurements(self) -> None:
        y_trues, y_pred = load_json(Y_TRUES_FILE), load_json(Y_PRED_FILE)
        measure = sk_measure(y_trues, y_pred)
        measures = load_json(MEASURES_FILE)
        self.assertDictEqual(confidence_score(measures), conf_95)
        self.assertDictEqual(confidence_score(measures, 0.99), conf_6_3_99)
        self.assertDictEqual(measures_mean(measures), mean)
        self.assertDictEqual(standard_deviation(measures), sd)
        self.assertDictEqual(standard_error(measures), se)
        self.assertDictEqual(select_metrics(measure), {})
        self.assertDictEqual(select_metrics(measure, SIMPLE_ACCURACY, MACRO_RECALL, MACRO_F1, MACRO_JACCARD),
                             {'macro_f1': 0.6676911015978718, 'macro_jaccard': 0.6027144762993819,
                              'macro_recall': 0.7197663971248877, 'simple_accuracy': 0.7314814814814815})

    def test_uncertainty(self) -> None:
        measures_list = load_json(MEASURES_FILE)
        for measures in measures_list:
            self.assertFalse(has_confidence(measures))
        confidence = confidence_score(measures_list, 0.99)
        self.assertTrue(has_confidence(confidence))
        self.assertTupleEqual(min_uncertainty([confidence]),
                              ('balanced_accuracy', (0.695702864876455, 0.04531130036330688)))
        self.assertTupleEqual(max_uncertainty([confidence]),
                              ('micro_jaccard', (0.5316665991417848, 0.05862737753476288)))

    def test_min_and_max_values(self) -> None:
        measures_list = load_json(MEASURES_FILE)
        self.assertTupleEqual(min_value(measures_list), ('micro_jaccard', 0.5316665991417848))
        self.assertTupleEqual(max_value(measures_list), ('weighted_precision', 0.7389542915931806))
        confidence = confidence_score(measures_list, 0.99)
        confidence['micro_recall'] = (0.725, 0.01)
        confidence['macro_jaccard'] = (0.5584330739064476, 0.01373581918888226)
        self.assertListEqual(min_value([confidence]), [('micro_jaccard', 0.5316665991417848, 0.05862737753476288),
                                                       ('macro_jaccard', 0.5584330739064476, 0.01373581918888226),
                                                       ('weighted_jaccard', 0.602431880785639, 0.05138071188889759),
                                                       ('macro_f1', 0.6207920707004468, 0.05503931310763133)])
        self.assertListEqual(max_value([confidence]), [('weighted_precision', 0.7389542915931806, 0.05156424197771303),
                                                       ('micro_recall', 0.725, 0.01),
                                                       ('balanced_accuracy', 0.695702864876455, 0.04531130036330688),
                                                       ('simple_accuracy', 0.6925925925925926, 0.050312012833819586),
                                                       ('micro_f1', 0.6925925925925926, 0.050312012833819586),
                                                       ('micro_precision', 0.6925925925925926, 0.050312012833819586),
                                                       ('weighted_recall', 0.6925925925925926, 0.050312012833819586),
                                                       ('weighted_f1', 0.6897580626192598, 0.05122934800973333)])
        # plot_measure(confidence)
        # print(max_value([confidence]))

    # def test_plot(self) -> None:
    #     conf_95 = {
    #         'simple_accuracy': (0.6925925925925926, 0.03502136605451667),
    #         'balanced_accuracy': (0.695702864876455, 0.0315404522111038),
    #         'micro_f1': (0.6925925925925926, 0.03502136605451667),
    #         'macro_f1': (0.6207920707004468, 0.038311962156994395),
    #         'weighted_f1': (0.6897580626192598, 0.03565990800863161),
    #         'micro_precision': (0.6925925925925926, 0.03502136605451667),
    #         'macro_precision': (0.6386742183008606, 0.040704810624135446),
    #         'weighted_precision': (0.7389542915931806, 0.03589302220107715),
    #         'micro_recall': (0.6925925925925926, 0.03502136605451667),
    #         'macro_recall': (0.6509717507624115, 0.03941730649957531),
    #         'weighted_recall': (0.6925925925925926, 0.03502136605451667),
    #         'micro_jaccard': (0.5316665991417848, 0.040809554891851146),
    #         'macro_jaccard': (0.5584330739064476, 0.03740462144237966),
    #         'weighted_jaccard': (0.602431880785639, 0.035765269919655784)
    #     }
    #
    #     plot_measure(conf_95, conf_95)



if __name__ == '__main__':
    unittest.main()
