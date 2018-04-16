import unittest

from book.normal8 import *
from book.cf2 import raw2std

#用于生成推荐列表
train_user_item = {
    #         1  2  3  4  5  6  7  8  9  10
    "user1": [0, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    "user2": [1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    "user3": [0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    "user4": [0, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    "user5": [1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
    "user6": [1, 1, 1, 1, 0, 0, 1, 0, 0, 1],
    "user7": [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    "user8": [0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
    "user9": [0, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    "user10": [1, 1, 1, 0, 1, 0, 0, 1, 0, 0]
}

raw_data = {
    "user1": ["item1", "item2", "item3"],
    "user2": ["item1", "item4", "item5"],
    "user3": ["item2", "item6", "item7"],
    "user4": ["item3", "item4", "item6"],
    "user5": ["item5", "item6", "item7"]
}


class HotTest(unittest.TestCase):

    def test_most_pop_recommend(self):
        train = raw2std(train_user_item)
        result = most_popilarity_recommend(train)
        train2 = raw2std(raw_data)
        result2 = most_popilarity_recommend(train2)
        result3 = most_popilarity_recommend(train2,2)
        self.assertEqual(result.tolist(), [9, 1, 2, 6, 4, 0, 3, 8, 7, 5])
        self.assertEqual(result2.tolist(), ['item6', 'item7', 'item5', 'item4', 'item3', 'item2', 'item1'])
        self.assertEqual(result3.tolist(), ['item6', 'item7'])

    def test_recent_popularity(self):
        '''
        train = raw2std(train_user_item)
        result = most_popilarity_recommend(train)
        train2 = raw2std(raw_data)
        result2 = most_popilarity_recommend(train2)
        result3 = most_popilarity_recommend(train2,2)
        self.assertEqual(result.tolist(), [9, 1, 2, 6, 4, 0, 3, 8, 7, 5])
        self.assertEqual(result2.tolist(), ['item6', 'item7', 'item5', 'item4', 'item3', 'item2', 'item1'])
        self.assertEqual(result3.tolist(), ['item6', 'item7'])
        '''

if __name__ == '__main__':
    unittest.main()
