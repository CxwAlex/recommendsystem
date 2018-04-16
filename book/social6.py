#社会化推荐： familiarity 存储了每个用户最熟悉的 K 个好友和他们的熟悉程度，
#similarity 存储了和每个用户兴趣最相关的 K 好友和他们的兴趣相似度。
#train 记录了每个用户的行为记录，其中 train[u] 记录了用户 u 喜欢的物品列表

#todo:本章的核心问题是如何表达该社交网络图，有没有成熟的解决方案
#todo:目前暂时使用矩阵的方式表示
#我们用图G(V,E,w)定义一个社交网络，+
# 其中V是顶点集合，每个顶点代表一个用户，
# E是边集合，如果用户va和vb有社交网络关系，那么就有一条边e(va, vb)连接这两个用户，
# 而 w(va, vb)定义了边的权重。
#todo:表达社交关系的图是使用单项还是双向——考虑到后期的可扩展性，即有向图；还是使用单项吧
import math
from pandas import Series, DataFrame
from book.cf2 import list2matrix, count_set

#根据具体的结构在完善，首先需要具备基础的将字典列表转换为dataframe的能力
def graph2dataframe(graph):
    result = DataFrame(list2matrix(graph), index= graph.keys())
    return result


def matrix2dataframe(matrix):
    if isinstance(matrix, dict):
        result = DataFrame(matrix, index = matrix.keys())
    elif isinstance(matrix, list):
        result = DataFrame(matrix)
    return result





#todo:弄清楚python有没有形参实参的概念，函数分开写会不会造成内存浪费
def social_similarity(dataframe, user=None, filter=True):
    for u in dataframe.columns[0:1]:
        for v in dataframe.columns[1:2]:
            if dataframe[u][v] == dataframe[v][u]:
                similarity = similarity_no_direction(dataframe, user, filter)
            else:
                similarity = similarity_have_direction(dataframe, user, filter)

    return similarity

#计算用户相似度并给用户推荐朋友
#todo：计算相似度单独拿出来——相似度可以用来推荐无物品，也可以用来推荐朋友

#无向社交网络，根据共同好友比例计算相似度
#todo:此处的定义，相似度怎么算
#todo:是否返回推荐列表
#todo:分析有向无向的区别，如果已经在前期数据集表示的时候就已经去区分开来，那后续是否要区分
#todo:重新审视下面这段函数的index和columns的关系
#todo:相似度矩阵不对称：查看问题:无向图构建的时候不对称
#此处定义使用的是社交网络里的out来计算相似度，也可以使用in，在无向社交网络里两者相等
def similarity_no_direction(dataframe, user= None, filter= True):
    if user:
        similarity = Series(0.0, index= dataframe.index)
        for v in dataframe.index:
            if user == v or dataframe[user][v] == 1:
                if filter:
                    continue
                else:
                    similarity[v] += 1
                continue
            similarity[v] += count_set(dataframe[user] & dataframe.ix[v]) / \
                                math.sqrt(1.0 * count_set(dataframe[user]) * count_set(dataframe.ix[v]))
    else:
        similarity = DataFrame(0.0, index= dataframe.index, columns= dataframe.columns)
        for u in dataframe.columns:
            for v in dataframe.index:
                if u == v or dataframe[u][v] == 1:
                    if filter:
                        similarity[u][v] = 0
                    else:
                        similarity[u][v] = 1
                    continue
                similarity[u][v] += count_set(dataframe[u]&dataframe.ix[v]) / \
                                    math.sqrt(1.0 * count_set(dataframe[u]) * count_set(dataframe.ix[v]))

    return similarity


#有针对性的改写：
#dataframe中，columns即为out数据，index即为in数据
#有向网络中的相似度计算：u和v的相似度计算——u关注的人中有多少也关注了v

#有向社交网络中的相似度
def similarity_have_direction(dataframe, user= None, filter= True):
    if user:
        similarity = Series(0.0, index=dataframe.index)
        for v in dataframe.index:
            if user == v or dataframe[user][v] == 1:
                if filter:
                    continue
                else:
                    similarity[v] += 1
                continue
            result = 0
            for i in dataframe.columns:
                # 如果u没有关注过i，那么则跳过
                if dataframe[user][i] == 0:
                    continue
                if dataframe[i][v] == 1:
                    result += 1
            similarity[v] = result / math.sqrt(1.0 * count_set(dataframe[user]) * count_set(dataframe.ix[v]))
    else:
        similarity = DataFrame(0.0, index=dataframe.index, columns=dataframe.columns)
        for u in dataframe.columns:
            for v in dataframe.index:
                if u == v or dataframe[u][v] == 1:
                    if filter:
                        similarity[u][v] = 0
                    else:
                        similarity[u][v] = 1
                    continue
                result = 0
                for i in dataframe.columns:
                    #如果u没有关注过i，那么则跳过
                    if dataframe[u][i] == 0:
                        continue
                    if dataframe[i][v] == 1:
                        result += 1
                similarity[u][v] = result / math.sqrt(1.0 * count_set(dataframe[u]) * count_set(dataframe.ix[v]))

    return similarity



def sort_similarity_and_rank(dataframe, user=None, N=None):
    if user:
        if N:
            result = dataframe.sort_values(ascending=False).index[0:N]
        else:
            result = dataframe.sort_values(ascending=False).index
    else:
        if N:
            result= DataFrame(columns= dataframe.columns)
            for u in dataframe.columns:
                result[u] = dataframe[u].sort_values(ascending=False).index[0:N]
        else:
            result = DataFrame(columns=dataframe.columns)
            for u in dataframe.columns:
                result[u] = dataframe[u].sort_values(ascending=False).index

    return result


def FriendSuggestion(dataframe, N=None, user=None, filter=True):
    similarity = social_similarity(dataframe, user, filter)
    suggestion = sort_similarity_and_rank(similarity, user, N)
    return suggestion



#基于社交关系的推荐
#接口怎么设计
def Recommend(dataframe_social, dataframe_item, user = None, N = None, filter = True):
    similarity_uu = social_similarity(dataframe_social, user)
    if user:
        rank = Series(0.0, index=dataframe_item.index)
        for v in dataframe_social.columns:
            if user == v or similarity_uu[user][v] == 0:
                continue
            for i in dataframe_item.index:
                if dataframe_item[v][i] == 0 or dataframe_item[user][i] != 0:
                    continue
                rank[i] += similarity_uu[user][v] * dataframe_item[v][i]
    else:
        rank = DataFrame(0.0, index=dataframe_item.index, columns=dataframe_social.columns)
        for u in dataframe_social.columns:
            for v in dataframe_social.columns:
                if u == v or similarity_uu[u][v] == 0:
                    continue
                for i in dataframe_item.index:
                    if dataframe_item[v][i] == 0 or dataframe_item[u][i] != 0:
                        continue
                    rank[u][i] += similarity_uu[u][v] * dataframe_item[v][i]

    result = sort_similarity_and_rank(rank, user, N)
    return result
