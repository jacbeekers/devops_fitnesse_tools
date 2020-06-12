import unittest

from test.test_createFitNesseArtifact import TestFitNesseArtifact
from test.test_walk import TestWalk


class TestAll(unittest.TestCase):
    def test_all(self):
        suite1 = TestWalk.walk_suite(self)
        suite2 = TestFitNesseArtifact.fitnesse_suite(self)
        product1_suite = TestFitNesseArtifact.fitnesse_product1_suite(self)
        all_products_suite = TestFitNesseArtifact.fitnesse_all_products_suite(self)
        alltests = unittest.TestSuite((suite1, suite2, product1_suite, all_products_suite))
        print('#Test cases: ' + str(alltests.countTestCases()))

if __name__ == '__main__':
    unittest.main()
