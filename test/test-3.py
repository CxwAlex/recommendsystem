# encoding=utf-8
import unittest

from book.cf2 import *


#构造原始数据集
raw_data1 = {
    "user1": ["item1", "item2", "item3"],
    "user2": ["item1", "item4", "item5"],
    "user3": ["item2", "item6", "item7"],
    "user4": ["item3", "item4", "item6"],
    "user5": ["item5", "item6", "item7"]
}

raw_data2 = {
    "user1": [1, 1, 1, 0, 0, 0, 0],
    "user2": [1, 0, 0, 1, 1, 0, 0],
    "user3": [0, 1, 0, 0, 0, 1, 1],
    "user4": [0, 0, 1, 1, 0, 1, 0],
    "user5": [0, 0, 0, 0, 1, 1, 1]
}
std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7"]

std_data = raw2std(raw_data2, index= std_index)

class SimilarityTest(unittest.TestCase):

    def test_usersimilarity(self):
        train = std_data
        similarity = UserSimilarity(train)
        self.assertEqual(similarity["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity["user1"]["user2"], 0.3333333)

if __name__ == '__main__':
    unittest.main()
