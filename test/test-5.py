# encoding=utf-8
import unittest
import pandas

from book.context5 import *
from book.cf2 import raw2std

#三元组

raw_data = [
    [1, 1, 0],
    [1, 2, 1],
    [1, 3, 4],
    [1, 7, 5],
    [1, 9, 7],
    [2, 9, 0],
    [2, 2, 4],
    [2, 5, 8],
    [3, 2, 5],
    [3, 7, 7],
    [3, 1, 0],
    [3, 6, 1],
    [3, 3, 4],
    [3, 8, 5],
    [3, 9, 7],
    [4, 6, 7],
    [4, 2, 3],
    [5, 3, 1],
    [5, 7, 5],
    [5, 9, 7],
    [5, 4, 0],
    [6, 2, 4],
    [6, 5, 8],
    [6, 9, 5],
    [7, 7, 7],
    [7, 1, 0],
    [7, 6, 1],
    [7, 3, 4],
    [7, 8, 5],
    [7, 9, 7]
]

raw_data1 = [
    ["user1", "item1", 0],
    ["user1", "item5", 1],
    ["user2", "item2", 0],
    ["user2", "item3", 2],
    ["user2", "item5", 5],
    ["user3", "item1", 2],
    ["user3", "item3", 3],
    ["user3", "item4", 4]
]

#todo:利用正式的带有日期的数据进行测试

raw_data2 = [
    [1, 1, 0],
    [1, 2, 1],
    [1, 3, 4],
    [1, 7, 5],
    [1, 9, 7],
    [2, 9, 0],
    [2, 2, 4],
    [2, 5, 8],
]


'''
#构造原始数据集
raw_data_user = {
    "user1": [["item2",""], "item4", "item9"],
    "user2": ["item1"],
    "user3": ["item6", "item4"],
    "user4": ["item1", "item3", "item7"],
    "user5": ["item8", "item9"],
    "user6": ["item3"],
    "user7": ["item4", "item8", "item10"],
    "user8": ["item5", "item7"],
    "user9": ["item1", "item5", "item10"],
    "user10": ["item7", "item9"],
}

'''

class TransformTest(unittest.TestCase):

    def test_list2dataframe_time(self):
        dataframe1 = list2dataframe_time(raw_data)
        self.assertEqual(dataframe1[1].values.tolist()[0:3], [0, 1, 4])
        dataframe2 = list2dataframe_time(raw_data1)
        self.assertEqual(dataframe2["user2"]["item5"], 5)


    def test_get_columns_and_index(self):
        dataframe1 = get_columns_and_index(raw_data)
        dataframe2 = get_columns_and_index(raw_data1)
        self.assertEqual(dataframe1[0], {1, 2, 3, 4, 5, 6, 7})
        self.assertEqual(dataframe2[0], {'user1', 'user2', 'user3'})





class ContextSimilarityTest(unittest.TestCase):

    def test_itemsimilarity(self):
        train = list2dataframe_time(raw_data)
        dataframe1 = ItemSimilarity(train, 0.6)
        self.assertEqual(dataframe1[1][1], 1)
        self.assertEqual(dataframe1[4][3], 0.3125)

        train2 = list2dataframe_time(raw_data1)
        dataframe2 = ItemSimilarity(train2, 0.6)
        self.assertAlmostEqual(dataframe2["item5"]["item2"], 0.17677669)
        self.assertAlmostEqual(dataframe2["item4"]["item3"], 0.44194173)

    def test_usersimilarity(self):
        train1 = list2dataframe_time(raw_data1)
        dataframe1 = UserSimilarity(train1, 0.6)
        self.assertAlmostEqual(dataframe1["user2"]["user3"], 0.20833333)
        self.assertAlmostEqual(dataframe1["user1"]["user3"], 0.18556740)
        train2 = list2dataframe_time(raw_data)
        dataframe2 = UserSimilarity(train2, 0.6)
        self.assertAlmostEqual(dataframe2[1][2], 0.14186752)
        self.assertAlmostEqual(dataframe2[4][6], 0.25515518)

class ContextRecommendTest(unittest.TestCase):

    def test_recommend1(self):
        train = list2dataframe_time(raw_data1)
        rank = Recommendation(train, t0=10)
        self.assertAlmostEqual(rank["user1"]["item4"], 0.02921928)
        train1 = list2dataframe_time(raw_data)
        rank1 = Recommendation(train1, t0=10)
        self.assertAlmostEqual(rank1[1][4], 0.0851035)

    def test_recommend2(self):
        train = list2dataframe_time(raw_data1)
        rank = Recommend(train, t0=10)
        self.assertAlmostEqual(rank["user1"]["item4"], 0.01944039)
        train1 = list2dataframe_time(raw_data)
        rank1 = Recommend(train1, t0=10)
        self.assertAlmostEqual(rank1[1][4], 0.04573775)

if __name__ == '__main__':
    unittest.main()
