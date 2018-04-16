# encoding=utf-8
import unittest
from book.num1 import *


#records[i] = [u, i, rui, pui]
records = [
    [1, 1, 2, 0],
    [1, 2, 1, 1],
    [2, 1, 0, 0],
    [2, 2, 0, 0]
]

test = [
    [1,[1,1,1,1],[0,0,1,1]],
    [2,[0,0,0,0],[1,1,0,0]]
]

p1 = [
    [1, 0.5],
    [2, 0.5]
]
class NumTest(unittest.TestCase):

    def test_rmse_and_mae(self):
        rmse = RMSE(records)
        mae = MAE(records)
        self.assertEqual(rmse, 1)
        self.assertEqual(mae, 0.5)

    def test_precision_and_recall(self):
        result = PrecisionRecall(test, 4)
        precison = result[0]
        recall = result[1]
        self.assertEqual(precison, 0.5)
        self.assertEqual(recall, 0.5)
    '''
    def test_gini(self):
        gini1 = GiniIndex(p1)
        #mae = MAE(records)
        self.assertEqual(gini1, 0)
        #self.assertEqual(mae, 6)
    '''

if __name__ == '__main__':
    unittest.main()
