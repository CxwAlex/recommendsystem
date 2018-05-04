# encoding=utf-8
import unittest

from book.tag4 import *

#构造原始数据集
raw_data1 = {
    "user1": ["如何学习python", "如何使用python编程", "Spark核心技术"],
    "user2": ["刀剑神域", "微波炉菜谱", "如何做饭"],
    "user3": ["Hadoop核心技术", "大数据处理", "刀剑神域"],
    "user4": ["python进行数据分析", "R语言数据分析", "大数据数据分析"],
    "user5": ["刀剑神域", "龙泉刀剑", "天线宝宝"]
}

item_tag ={
    "如何学习python":["python", "编程", "自学"],
    "如何使用python编程":["python", "编程", "自学"],
    "python进行数据分析":["python", "编程", "数据分析"],
    "大数据处理":["大数据", "Hadoop", "Spark"],
    "R语言数据分析":["R", "编程", "数据分析"],
    "大数据数据分析":["大数据", "数据分析"],
    "Hadoop核心技术":["Hadoop", "大数据"],
    "Spark核心技术":["Spark", "大数据"],
    "刀剑神域":["动画片", "刀剑"],
    "龙泉刀剑":["刀剑", "商品"],
    "天线宝宝":["动画片", "儿童"],
    "微波炉菜谱":["做饭", "生活", "菜谱"],
    "如何做饭":["做饭", "自学", "生活"]
}

tag_item ={
    "python":["如何学习python","如何使用python编程","python进行数据分析"],
    "编程":["如何学习python","如何使用python编程","python进行数据分析","R语言数据分析"],
    "自学":["如何学习python","如何使用python编程","如何做饭"],
    "数据分析":["python进行数据分析","R语言数据分析","大数据数据分析"],
    "大数据":["大数据处理","大数据数据分析","Hadoop核心技术","Spark核心技术"],
    "R":["R语言数据分析"],
    "Hadoop":["大数据处理","Hadoop核心技术"],
    "Spark":["大数据处理","Spark核心技术"],
    "动画片":["刀剑神域","天线宝宝"],
    "刀剑":["刀剑神域","龙泉刀剑"],
    "儿童":["天线宝宝"],
    "做饭":["微波炉菜谱","如何做饭"],
    "生活":["微波炉菜谱","如何做饭"],
    "菜谱":["微波炉菜谱"]
}

user_item_tag = [
    ["user1", "如何学习python", ["python", "编程", "自学"]],
    ["user1", "如何使用python编程", ["python",  "编程"]],
    ["user2", "Hadoop核心技术", ["Hadoop", "大数据"]],
    ["user2", "python进行数据分析", ["python", "数据分析"]],
    ["user2", "大数据数据分析", ["大数据", "数据分析"]],
    ["user3", "刀剑神域", ["动画片", "刀剑"]],
    ["user3", "如何学习python", ["python"]],
    ["user3", "微波炉菜谱", ["做饭", "生活", "菜谱"]]
]

class ToolTest(unittest.TestCase):

    def test_get_user_tags(self):
        train = get_user_tags(user_item_tag)
        #print("test_get_user_tags")
        #print(train)

        self.assertEqual(train["user2"]["数据分析"], 2)

    def test_get_item_tags(self):
        train = get_item_tags(user_item_tag)
        #print("test_get_item_tags")
        #print(train)

        self.assertEqual(train["如何学习python"]["python"], 2)

    def test_get_user_item(self):
        train = get_user_item(user_item_tag)
        #print("test_get_item_tags")
        #print(train)

        self.assertEqual(train["user3"]["微波炉菜谱"], 1)

    def test_count_tags(self):
        train = count_tags(user_item_tag)
        #print("test_count_tags")
        #print(train)

        self.assertEqual(train["python"], 4)

    def test_item_and_tag_to_dataframe(self):
        train = item_and_tag_to_dataframe(item_tag)
        train1 = item_and_tag_to_dataframe(tag_item)
        #print("test_item_and_tag_to_dataframe")
        #print(train)

        self.assertEqual(train["如何学习python"]["python"], 1)
        self.assertEqual(train1["python"]["如何学习python"], 1)

    def test_item_and_tag_transform(self):
        train = item_and_tag_transfrom(item_tag)
        train1 = item_and_tag_transfrom(tag_item)
        #print("test_item_and_tag_transform")
        #print(train)

        self.assertEqual(train['python'], ['如何学习python', '如何使用python编程', 'python进行数据分析'])
        self.assertEqual(train1['如何学习python'], ['python', '编程', '自学'])


    def test_split_data(self):
        train,test = SplitData(user_item_tag)
        #print("test_split_data")
        #print(train)
        #print(test)

    def test_item_similarity(self):
        item_tags = get_item_tags(user_item_tag)
        item_sim = item_similarity(item_tags)
        #print(item_sim)
        self.assertEqual(item_sim['如何使用python编程']['python进行数据分析'], 0.5)

    def test_Recommend(self):
        recommend = Recommend(user_item_tag, 'user1')
        self.assertEqual(recommend['python进行数据分析'], 2)

class RecommendTagTest(unittest.TestCase):

    def test_popular_tag(self):
        tags = count_tags(user_item_tag)
        rank = RecommendPopularTags(tags)
        rank2 = RecommendPopularTags(tags, 2)
        self.assertEqual(rank, ['python'])
        self.assertEqual(rank2[0:1], ['python'])

    def test_item_popular_tag(self):
        item_tag = get_item_tags(user_item_tag)
        rank = RecommendItemPopularTags(item_tag, '如何学习python')
        self.assertEqual(rank, ['python'])

    def test_user_popular_tag(self):
        user_tag = get_user_tags(user_item_tag)
        rank = RecommendUserPopularTags(user_tag, 'user1', 2)
        self.assertEqual(set(rank), {'python', '编程'})

    def test_hybrid_popular_tag(self):
        item_tag = get_item_tags(user_item_tag)
        user_tag = get_user_tags(user_item_tag)
        result1 = RecommendHybridPopularTags('user2', '刀剑神域', user_tag, item_tag,N=2)
        #print(set(result1))
        self.assertAlmostEqual(set(result1), {'大数据', '数据分析'})


if __name__ == '__main__':
    unittest.main()
