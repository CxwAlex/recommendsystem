#todo:把过程中的一些参数单独提取出来，做到接口里，方便调参
import math
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from book.cf2 import count_set

#这个地方专管三元组的转换
def list2dataframe_time(train, columns= None, index= None):
    #todo:这个地方不太好写啊
    #todo:1要对多种数据进行处理
    #todo:2决定好到底要使用什么形式的矩阵
    #列表套列表
    if (not index) and (not columns):
        columns, index = get_columns_and_index(train)
    elif not columns:
        index = get_columns_and_index(train)[0]
    elif not index:
        index = get_columns_and_index(train)[1]

    #单矩阵方案
    user_item_time = DataFrame(index= index, columns= columns)
    for a in train:
        u=a[0]
        i=a[1]
        t=a[2]
        user_item_time[u][i] = t
    return user_item_time

#获取三元组数据的行和列
def get_columns_and_index(train):

    # todo:如何解决顺序问题
    u = set()
    i = set()
    for a in train:
        u.add(a[0])
        i.add(a[1])
    return u, i

def count_set_nan(train):
    count = 0
    for i in train:
        if not np.isnan(i):
            count += 1

    return count

#加入时间上下文后的基于物品的推荐
#todo:此处出错是因为N的计算错误，之前是非0计算，现在应该是非nan计算
def ItemSimilarity(train, alpha = 1.0):
    #calculate co-rated users between items
    C = DataFrame(0.0, index=train.index, columns=train.index)
    N = train.apply(func=count_set_nan, axis=1)
    for u in train.columns:
        items = train.index[train[u].notnull()]
        for i in items:
            for j in items:
                C[i][j] += 1 / (1 + alpha * abs(train[u][i] - train[u][j]))

    # calculate finial similarity matrix W
    W = DataFrame(0.0, index=train.index, columns=train.index)
    for i in train.index:
        #下面是针对每一列进行归一化，但是会导致矩阵不对称问题
        for j in train.index:
            #归一化
            W[i][j] = (C[i][j] / math.sqrt(N[i] * N[j]))
    return W

#考虑时间因素后的用户相似度（对共同的兴趣引入时间衰减因子）
def UserSimilarity(train, alpha = 1.0):
    #calculate co-rated items between users
    C = DataFrame(0.0, index=train.columns, columns=train.columns)
    for i in train.index:
        users = train.columns[train.ix[i].isnull() == False]
        #获取在i上行为不为NAN的user列表
        for u in users:
            for v in users:
                if u == v:
                    continue
                C[u][v] += 1 / (1 + alpha * abs(train[u][i] - train[v][i]))

    #todo:如何将nan值简单转换成逻辑值
    #此处为直接使用user_item计算两者相似度
    w = DataFrame(index= train.columns, columns= train.columns)
    N = train.apply(func=count_set_nan, axis=0)

    for u in train.columns:
        for v in train.columns:
            #此处不判断，结果也是1，但是这样减少了后面乘除法的操作
            if u == v:
                w[u][v] = 1
                continue
            w[u][v] = C[u][v]/math.sqrt(N[u] * N[v] * 1.0)

    return w


#加大用户最近行为比重的推荐算法
def Recommendation(train, alpha=1.0, t0= None, user= None, N= None, k= None):
    W = ItemSimilarity(train, 0.6)

    #开始计算推荐物品
    rank = DataFrame(0.0, index=train.index, columns=train.columns)
    #u是目标用户，v是近邻用户，wuv是相似度
    #i是物品编号，rvi是v对i的兴趣
    if k:
        for u in train.columns:
            for j in train.index[train[u].isnull() == False]:
                for i in W[j].sort_values(ascending=False).index[1:k+1]:
                    if not np.isnan(train[u][i]) or W[i][j] == 0:
                        continue
                    else:
                        rank[u][i] += W[i][j] / (1 + alpha * (t0 - train[u][j]))
    else:
        for u in train.columns:
            #判断是不是null
            for j in train.index[train[u].isnull() == False]:
                for i in W[j].sort_values(ascending=False).index[1:]:
                    if not np.isnan(train[u][i]) or W[i][j] == 0:
                        continue
                    else:
                        rank[u][i] += W[i][j] / (1 + alpha * (t0 - train[u][j]))

    return rank



#考虑（考虑时间后）兴趣相似用户的最近兴趣
def Recommend(train, alpha=1.0, t0= None, user= None, N= None, k= None):
    W = UserSimilarity(train)

    #开始计算推荐物品
    rank = DataFrame(0.0, index=train.index, columns=train.columns)
    #u是目标用户，v是近邻用户，wuv是相似度
    #i是物品编号，rvi是v对i的兴趣
    if k:
        for u in train.columns:
            for v in W[u].sort_values(ascending=False).index[1:k]:
                for i in train[v].index[train[v].isnull() == False]:
                    if pd.isnull(train[u][i]) == False:
                        continue
                    rank[u][i] += W[u][v] / (1 + alpha * (t0 - train[v][i]))
    else:
        for u in train.columns:
            for v in W[u].sort_values(ascending=False).index[1:]:
                for i in train[v].index[train[v].isnull() == False]:
                    if pd.isnull(train[u][i]) == False:
                        continue
                    rank[u][i] += W[u][v] / (1 + alpha * (t0 - train[v][i]))


    return rank






