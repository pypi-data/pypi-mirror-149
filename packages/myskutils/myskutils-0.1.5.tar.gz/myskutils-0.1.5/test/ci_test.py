import unittest

from myskutils.ci import CI
from myskutils.metric import Metric


class MyTestCase(unittest.TestCase):
    def test_str(self) -> None:
        ci = CI(0.51, 0.12)
        self.assertEqual(str(ci), '0.51±0.12')
        self.assertEqual(repr(ci), 'CI(0.51, 0.12)')
        metric = Metric('Accuracy', ci)
        self.assertEqual(str(metric), 'Accuracy=0.51±0.12')
        self.assertEqual(repr(metric), 'Metric(\'Accuracy\', CI(0.51, 0.12))')

    def test_tuple(self) -> None:
        ci = CI(0.51, 0.12)
        self.assertEqual(tuple(ci), (0.51, 0.12))

    def test_ci_comparisons(self) -> None:
        ci1 = CI(1.5, 0.25)
        self.assertEqual(ci1.value, 1.5)
        self.assertEqual(ci1.ci, 0.25)
        self.assertEqual(ci1.min, 1.25)
        self.assertEqual(ci1.max, 1.75)
        self.assertIsNone(ci1.p)
        self.assertIsNone(ci1 ** 2)
        self.assertTupleEqual(ci1.interval, (1.25, 1.75))
        ci2 = CI.from_interval(2, 1.5, 0.05)
        self.assertEqual(ci2.value, 1.75)
        self.assertEqual(ci2.min, 1.5)
        self.assertEqual(ci2.max, 2)
        self.assertEqual(ci2.ci, 0.25)
        self.assertEqual(ci2.p, 0.05)
        self.assertEqual(ci2 ** 2, 0.0025000000000000005)
        self.assertFalse(ci1.is_significant(ci2))
        self.assertTupleEqual(ci2.interval, (1.5, 2))
        ci3 = CI(1, 0.25, 0.01)
        ci4 = CI(1, 0.25, 0.01)
        self.assertTrue(ci2.is_significant(ci3))
        self.assertTrue(ci3.is_significant(ci2))
        self.assertTrue(ci4 == ci3)
        self.assertFalse(ci4 != ci3)
        self.assertTrue(ci2 > ci3)
        self.assertTrue(ci1 > ci3)
        self.assertTrue(ci1 >= ci3)
        self.assertFalse(ci1 <= ci3)
        self.assertFalse(ci1 < ci3)
        self.assertTupleEqual(tuple(ci1), (1.5, 0.25))
        self.assertTrue(ci1)
        self.assertTrue(ci2)
        self.assertFalse(CI(0, 0))
        self.assertEqual(float(ci1), 1.5)
        self.assertEqual(float(ci2), 1.75)
        self.assertEqual(hash(ci1), 3808642330255693810)
        self.assertNotIn(ci1, ci2)
        self.assertIn(CI(1.6, 0.1), ci1)
        self.assertIn(CI(1.5, 0.25), ci1)
        self.assertEqual(complex(1.5, 0.25), complex(ci1))


if __name__ == '__main__':
    unittest.main()
