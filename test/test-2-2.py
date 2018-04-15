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

    def test_user_similarity_back(self):
        train = std_data
        similarity_back = UserSimilarityBack(train)
        self.assertEqual(similarity_back["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity_back["user1"]["user2"], 0.3333333)

    def test_usersimilarity_down_hot(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index= std_index)
        rank = UserSimilarity_down_hot(train)
        self.assertAlmostEqual(rank["user1"]["user2"], 0.39509830)

    def test_itemsimilarity(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index= std_index)
        result = ItemSimilarity(train)
        self.assertAlmostEqual(result["item1"]["item5"], 0.66666666)

    def test_itemsimilarity_down_hot(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index=std_index)
        result = ItemSimilarity_down_hot(train)
        #归一化之后的
        #self.assertAlmostEqual(result["item1"]["item8"], 0.56125476)
        #未归一化的
        self.assertAlmostEqual(result["item1"]["item8"], 0.29669934)



class UserCFTest(unittest.TestCase):

    def test_user_recommend(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index= std_index)
        rank = Recommend(train, 2, 5, sort = False)
        self.assertAlmostEqual(rank["user1"]["item5"], 0.66666666)
        result = Recommend(train, 2, 3)
        self.assertEqual(result["user1"][0], "item8")

    def test_recommendation_itemcf(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index=std_index)
        rank = Recommendation_itemcf(train,3)
        self.assertAlmostEqual(rank["user1"]["item5"], 3.15470053)


    def test_recommendation(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index=std_index)
        rank, rank_reason = Recommendation(train)
        self.assertAlmostEqual(rank["user1"]["item5"], 3.15470053)
        pat = "用户user1喜欢item1，物品item1和item5相似度为0.666666666667；用户user1喜欢item2，物品item2和item5相似度为0.57735026919；用户user1喜欢item3，物品item3和item5相似度为0.57735026919；用户user1喜欢item7，物品item7和item5相似度为0.666666666667；用户user1喜欢item10，物品item10和item5相似度为0.666666666667；"
        self.assertEqual(rank_reason["user1"]["item5"], pat)

    def test_PersonalRank(self):
        train = {
            #         1  2  3  4  5  6  7  8  9  10
            "user1": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
            "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            "user3": [0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
            "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            "user5": [1, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        }
        std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9", "item10"]
        train = raw2std(train, index=std_index)
        rank = PersonalRank(train, 0.8, 10000)
        self.assertAlmostEqual(rank["user1"]["item1"], 0)
        self.assertAlmostEqual(rank["user1"]["item5"], 0.4280)


if __name__ == '__main__':
    unittest.main()
