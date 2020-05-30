import unittest

from test.walk import Walk


class TestWalk(unittest.TestCase):
    def test_walk_current_directory(self):
        self.item = '.'
        walk = Walk()
        self.directory_counter, self.file_counter = walk.walk_through(self.item)
        self.assertGreater(self.file_counter, 0, 'walk through for >' + self.item + '< did not return any values')

    def test_walk_specific_file(self):
        self.filename = 'walk.py'
        walk = Walk()
        self.directory_counter, self.file_counter = walk.walk_through(self.filename)
        self.assertEqual(self.file_counter, 0,
                         'walk through for >' + self.filename + '< should not have returned a result.')

    def walk_suite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestWalk("test_walk_current_directory"))
        suite.addTest(TestWalk("test_walk_specific_file"))
        return suite
