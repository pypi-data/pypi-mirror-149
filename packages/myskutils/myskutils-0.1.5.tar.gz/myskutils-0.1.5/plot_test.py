import unittest

from mysutils.file import load_json

from myskutils.measure import filter_measure
from myskutils.metrics import WEIGHTED_F1, BALANCED_ACCURACY, SIMPLE_ACCURACY
from myskutils.plot import plot_figure


class MyTestCase(unittest.TestCase):
    def test_plot(self):
        data6_3 = load_json('../question-and-answer-server/results-6.3-2021-12-10.json')
        data6_6 = load_json('../question-and-answer-server/results-6.6-2021-12-10.json')
        data6_3 = filter_measure(data6_3, SIMPLE_ACCURACY, BALANCED_ACCURACY, WEIGHTED_F1)
        data6_6 = filter_measure(data6_6, SIMPLE_ACCURACY, BALANCED_ACCURACY, WEIGHTED_F1)
        data = {
            'v6.3': data6_3,
            'v6.6': data6_6
        }
        fig = plot_figure(data)
        fig.show()


if __name__ == '__main__':
    unittest.main()
