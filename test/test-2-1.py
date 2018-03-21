# encoding=utf-8
import unittest
import os

from book.cf2 import *

class SplitDataTest(unittest.TestCase):

    def test_split_data(self):
        data = [
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1], [1, 1], [1, 1]
        ]
        result = SplitData(data, 10, 3)
        len_train = len(result[0])
        len_test = len(result[1])
        #print(len_test, len_train)
        self.assertEqual(len_train, 66)

class DataTest(unittest.TestCase):

    def test_recall(self):
        train = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        test = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        recall = Recall(train, test, 3)
        self.assertEqual(recall, 1)


    def test_precision(self):
        train = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        test = {
            1: [0, 0, 0],
            2: [0, 0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0]
        }
        precision = Precision(train, test, 3)
        self.assertEqual(precision, 1)

    def test_coverage(self):
        train = {
            1: [0, 1, 2],
            2: [3, 4, 5],
            3: [6, 7, 8],
            4: [9, 0, 1]
        }
        coverage = Coverage(train, 3)
        self.assertEqual(coverage, 0.1)

    def test_popularity(self):
        train = {
            1: [0, 1, 2],
            2: [3, 4, 5],
            3: [6, 7, 8],
            4: [9, 0, 1]
        }
        popularity = Popularity(train, 3)
        print(popularity)
        #self.assertEqual(popularity, 1)


if __name__ == '__main__':
    unittest.main()
