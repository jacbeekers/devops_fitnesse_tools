import unittest

from test.test_createFitNesseArtifact import TestFitNesseArtifact
from test.test_walk import TestWalk


class TestAll(unittest.TestCase):
    def test_all(self):
        suite1 = TestWalk.walk_suite(self)
        suite2 = TestFitNesseArtifact.fitnesse_suite(self)
        alltests = unittest.TestSuite((suite1, suite2))
        print('#Test cases: ' + str(alltests.countTestCases()))

if __name__ == '__main__':
    unittest.main()
