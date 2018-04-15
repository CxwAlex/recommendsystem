# encoding=utf-8
import unittest

from book.coldstart3 import *


#构造原始数据集
raw_data1 = {
    "user1": ["如何学习python", "如何使用python编程", "Spark核心技术"],
    "user2": ["刀剑神域", "微波炉菜谱", "如何做饭"],
    "user3": ["Hadoop核心技术", "大数据处理", "刀剑神域"],
    "user4": ["python进行数据分析", "R语言数据分析", "大数据数据分析"],
    "user5": ["刀剑神域", "龙泉刀剑", "天线宝宝"]
}

std_index = ["item1", "item2", "item3", "item4", "item5", "item6", "item7"]

std_data = raw2std(raw_data2, index= std_index)

class SimilarityTest(unittest.TestCase):

    def test_usersimilarity(self):
        train = std_data
        similarity = CalculateSimilarity(train)
        self.assertEqual(similarity["user1"]["user5"], 0)
        self.assertAlmostEqual(similarity["user1"]["user2"], 0.3333333)

if __name__ == '__main__':
    unittest.main()
