# encoding=utf-8
import unittest

from book.cf2 import *

class SimilarityTest(unittest.TestCase):

    def test_usersimilarity(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4, 5, 6],
            2: [1, 2, 3, 5],
            3: [1, 3, 5, 6]
        }
        similarity = UserSimilarity(train)
        #print(similarity)
        self.assertEqual(similarity[0], [0, 0.25, 0.75, 0.5])


    def test_user_similarity_back(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

class UserCFTest(unittest.TestCase):

    def test_recommend(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4, 5, 6],
            2: [1, 2, 3, 5],
            3: [1, 3, 5, 6]
        }
        similarity = UserSimilarity(train)
        #print(similarity)
        self.assertEqual(similarity[0], [0, 0.25, 0.75, 0.5])


    def test_usersimilarity(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_itemsimilarity(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_recommendation(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_recommendation(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_itemsimilarity(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_RandomSelectNegativeSample(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_LatentFactorModel(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_Recommend(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

    def test_PersonalRank(self):
        train = {
            0: [0, 1, 2, 3],
            1: [0, 4],
            2: [1, 2, 3, 5],
            3: [1, 3]
        }
        similarity_back = UserSimilarityBack(train)
        #print(similarity_back)
        #self.assertEqual(similarity_back[0], [0, 0.25, 0.75, 0.5])

if __name__ == '__main__':
    unittest.main()
