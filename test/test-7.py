# encoding=utf-8
import unittest

from book.system7 import *


class SimilarityTest(unittest.TestCase):

    def test_RecommendationCore(self):
        self.assertEqual(similarity["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity["user1"]["user2"], 0.3333333)

    def test_sortByWeight(self):
        self.assertEqual(similarity["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity["user1"]["user2"], 0.3333333)

    def test_ReasonDiversity(self):
        self.assertEqual(similarity["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity["user1"]["user2"], 0.3333333)

if __name__ == '__main__':
    unittest.main()
