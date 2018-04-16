import random
import math
import numpy
from pandas import Series, DataFrame


# 获得用户对哪些物品产生过行为
# 将用户-物品表格转换为用户-物品-行为矩阵（0或1）
def list2matrix(raw_data):
    columns = []
    index = []
    for u, v_list in raw_data.items():
        if u in columns:
            pass
        else:
            columns.append(u)
        for v in v_list:
            if v in index:
                pass
            else:
                index.append(v)

    result = DataFrame(index= index, columns= columns)

    for u, v_list in raw_data.items():
        for i in index:
            if i in v_list:
                result[u][i] = 1
            else:
                result[u][i] = 0

    return result


#将原始的用户行为数据转化为标准化的矩阵格式
#支持的格式为上面两种
#可选参数std_index用来设置索引值
def raw2std(raw_data, index= []):
    mid_data = DataFrame(raw_data)
    if isinstance(mid_data[mid_data.columns[0]][mid_data.index[0]], (numpy.int64, numpy.float64)):
        if index:
            result = DataFrame(raw_data, index= index)
        else:
            result = DataFrame(raw_data)
    elif isinstance(mid_data[mid_data.columns[0]][mid_data.index[0]], str):
        result = list2matrix(raw_data)
    else:
        raise TypeError("not support data formart")
    #todo：三元组格式给出的结果
    return result

#获取推荐结果——待完善
def GetRecommendation(user, N):
    return [0]*N


#将数据集拆分成训练集和测试集的过程
#todo:该函数也需要完善，是将一部分人完全拿出，还是对每个用户拿出一部分进行测试
#
def SplitData(data, M, k, seed=0):
    test = []
    train = []
    random.seed(seed)
    for user, item in data:
        if random.randint(0,M) <= k:
            #randint随机生成0~M之间的数
            test.append([user,item])
        else:
            train.append([user,item])
    return train, test

#对于事后评估函数，统一使用dataframe进行评估
#todo:关于getrecommendation函数的编写

#计算准确率和召回率
def Recall(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user, N)
        for item in rank:
            if item in tu:
                hit += 1
        all += len(tu)
    return hit / (all * 1.0)

def Precision(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user, N)
        for item in rank:
            if item in tu:
                hit += 1
        all += N
    return hit / (all * 1.0)

#计算覆盖率
def Coverage(train, N):
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user]:
            all_items.add(item)
        rank = GetRecommendation(user, N)
        for item in rank:
            recommend_items.add(item)
    return len(recommend_items) / (len(all_items) * 1.0)

#计算新颖度
def Popularity(train, N):
    #首先计算不同物品的流行度
    item_popularity = dict()
    for user, items in train.items():
        for item in items:
            if item not in item_popularity:
                item_popularity[item] = 1
            item_popularity[item] += 1
    #接着计算推荐物品的流行度
    ret = 0
    n = 0
    for user in train.keys():
        rank = GetRecommendation(user, N)
        for item in rank:
            #print(item_popularity[item])
            #print(math.log(item_popularity[item]))
            ret += math.log(1 + item_popularity[item])
            n += 1
    ret /= n * 1.0
    return ret








#进来的数据已经是dataframe了

#计算单独一行中不为0的个数
def count_set(train):
    count = 0
    for i in train:
        if i != 0:
            count += 1

    return count

#计算余弦相似度
def UserSimilarity(train):
    w = DataFrame(index= train.columns, columns= train.columns)
    count_columns = train.apply(func=count_set, axis=0)

    for u in train.columns:
        for v in train.columns:
            if u == v:
                w[u][v] = 1
                continue

            w[u][v] = count_set(train[u] & train[v])
            w[u][v] /= math.sqrt(count_columns[u] * count_columns[v] * 1.0)
    return w


#利用倒排方法计算用户相似度
def UserSimilarityBack(train):
    train_item_user = train.T
    #calculate co-rated items between users
    #C表示u和v对拥有相同兴趣的物品数
    #N表示用户对物品产生行为的个数
    N = train_item_user.apply(func=count_set, axis=1)
    C = DataFrame(0, index=train.columns, columns=train.columns)
    for item in train_item_user.columns:
        for u in train_item_user.index:
            for v in train_item_user.index:
                if train_item_user[item][u] == 0 or train_item_user[item][v] == 0 or u == v:
                    continue
                else:
                    C[u][v] += 1

    #calculate finial similarity matrix W
    W = DataFrame(index=train_item_user.index, columns=train_item_user.index)
    for u in train_item_user.index:
        for v in train_item_user.index:
            if u == v:
                W[u][v] = 1
            else:
                W[u][v] = C[u][v] / math.sqrt(N[u] * N[v])
    return W


#惩罚了共同兴趣中的热门物品后的user-II的相似度计算
def UserSimilarity_down_hot(train):
    #calculate co-rated items between users
    C = DataFrame(0.0, index=train.columns, columns=train.columns)
    for item in train.index:
        #todo:此处的全columns循环改写为只对value不为0的user循环
        #已经得到了倒排表——使用内建表达式，效率高
        users = train.columns[train.ix[item] != 0]
        for u in users:
            for v in users:
                if u == v:
                    C[u][v] += 1
                    continue
                C[u][v] += 1 / math.log(1 + len(users))

    w = DataFrame(index= train.columns, columns= train.columns)
    N = train.apply(func=count_set, axis=0)

    for u in train.columns:
        for v in train.columns:
            #此处不判断，结果也是1，但是这样减少了后面乘除法的操作
            if u == v:
                w[u][v] = 1
                continue
            w[u][v] = C[u][v]
            w[u][v] /= math.sqrt(N[u] * N[v] * 1.0)
    return w


#todo:此处出现了分离，即两个在用户行为上完全一致的物品，其相似度不一样
#todo：主要是物品要跟自己相似，则自身相似度为1；但是一样行为的物品却因为热门惩罚系数降低
#todo：想一想这个问题如何解决——矩阵对称性重要，还是自身相似度为1重要
#惩罚活跃用户后的基于物品相似度的推荐算法
def ItemSimilarity_down_hot(train):
    # calculate co-rated users between items
    # 计算物品之间的相似性
    C = DataFrame(0.0, index=train.index, columns=train.index)
    N = train.apply(func=count_set, axis=1)
    users = Series(0.0, index= train.index)
    for item in train.index:
        users[item] = train.columns[train.ix[item] != 0]

    for u in train.columns:
        items = train.index[train[u] != 0]
        for i in items:
            for j in items:
                #if i == j:
                #    C[i][j] += 1
                #   continue
                C[i][j] += 1 / math.log(1 + len(items) * 1.0)

    # calculate finial similarity matrix W
    W = DataFrame(0.0, index=train.index, columns=train.index)
    std_W = Series(0.0,index= train.index)
    for i in train.index:
        #下面是针对每一列进行归一化，但是会导致矩阵不对称问题
        #std_W[i] = C[i][i] / math.sqrt(N[i] * N[i])
        for j in train.index:
            #归一化
            #W[i][j] = (C[i][j] / math.sqrt(N[i] * N[j]))/std_W[i]
            W[i][j] = (C[i][j] / math.sqrt(N[i] * N[j]))
    return W


#物品相似度
def ItemSimilarity(train):
    #calculate co-rated users between items
    #计算物品之间的相似性
    C = DataFrame(0.0, index=train.index, columns=train.index)
    N = train.apply(func=count_set, axis=1)
    for u in train.columns:
        items = train.index[train[u] != 0]
        for i in items:
            for j in items:
                #有针对性的决定是否包含元素本身
                if i == j:
                    C[i][j] += 1
                    continue
                C[i][j] += 1

    #calculate finial similarity matrix W
    W = DataFrame(0.0, index=train.index, columns=train.index)
    for i in train.index:
        for j in train.index:
            W[i][j] = C[i][j] / math.sqrt(N[i] * N[j])
    return W




# userCF推荐算法_只可指定k个近邻，不保证推荐k个物品
# train:训练集;k:k个近邻;N:TopN推荐;
# sort:是否排序，默认排序;filter：是否过滤掉已经有行为的物品，默认过滤。
#todo:待补充功能——指定k个物品&排序&对已经存在的物品进行删除
def rank_recommend_score(train, k):
    #W是用户之间的兴趣相似度, k是邻居数目
    W = UserSimilarity(train)

    #开始计算推荐物品
    rank = DataFrame(0.0, index=train.index, columns=train.columns)
    #u是目标用户，v是近邻用户，wuv是相似度
    #i是物品编号，rvi是v对i的兴趣
    for u in train.columns:
        for v in W[u].sort_values(ascending=False).index[1:k+1]:
            for i in train[v].index:
                #print(v, i, train[v][i])
                if train[v][i] == 0:
                    rank[u][i] += 0
                else:
                    rank[u][i] += W[u][v] * train[v][i]
    return rank

#若排序则返回排序后的推荐结果，否则返回推荐分数矩阵
def Recommend(train, k, N = None, sort = True, filter = True):
    rank = rank_recommend_score(train,k)
    #是否过滤掉已经有行为的物品
    if filter:
        for u in train.columns:
            for i in train.index:
                if train[u][i] == 1:
                    rank[u][i] = 0

    #是否排序&是否TopN推荐
    if sort:
        if N:
            result = DataFrame(columns=train.columns)
            for u in train.columns:
                result[u] = rank[u].sort_values(ascending=False).index[0:N]
        else:
            result = DataFrame(columns=train.columns)
            for u in train.columns:
                result[u] = rank[u].sort_values(ascending=False).index
        return result
    else:
        return rank


#todo：后续加入的功能，限制对象的数目，提升效率
#todo:整合成一整个推荐系统
#todo:要不要一开始就过滤掉在用户列表里的物品的计算，可以省下计算资源和时间

#基于物品相似度的推荐
#首先要计算物品之间的相似性
#然后再生成推荐列表
def Recommendation_itemcf(train, K):
    #首先获得物品相似度矩阵
    item_similarity = ItemSimilarity(train)

    #对用户列表里的每一个物品，计算其相关物品的推荐结果
    rank = DataFrame(0.0, index = train.index, columns = train.columns)
    for u in train.columns:
        for i in train.index[train[u] != 0]:
            for j in item_similarity.index[item_similarity[i] != 0]:
                #此处因为单独取出了不为0的物品，所以没有必要查重了
                #但是以后要是有评分或者权重的时候，还是需要的
                rank[u][j] += train[u][i] * item_similarity[i][j]
    return rank

#todo：感觉不好实现，两种方式：1使现有的数据结构膨胀，2使用额外的变量来保存理由
#带解释的基于物品的推荐
def Recommendation(train):
    #首先获得物品相似度矩阵
    item_similarity = ItemSimilarity(train)

    #对用户列表里的每一个物品，计算其相关物品的推荐结果
    rank = DataFrame(0.0, index= train.index, columns= train.columns)
    rank_reason = DataFrame("" ,index= train.index, columns= train.columns)
    for u in train.columns:
        for i in train.index[train[u] != 0]:
            for j in item_similarity.index[item_similarity[i] != 0]:
                #此处因为单独取出了不为0的物品，所以没有必要查重了
                #但是以后要是有评分或者权重的时候，还是需要的
                rank[u][j] += train[u][i] * item_similarity[i][j]
                rank_reason[u][j] += ("用户" + u + "喜欢" + i + "，物品" + i + "和" + j + "相似度为" + str(item_similarity[i][j]) + "；")
    return rank, rank_reason

#基于图的随机游走算法
#train是训练集，p是每次漫步的继续的随机数，即有p的概率继续向下走
# N是每个用户重复训练的次数, is_P决定返回是概率还是频率，默认概率
def PersonalRank(train, p, N, is_P = True, filter_item = True):
    #首先需要一个数据结构，用来表示原有的图，此处先用了两个数据结构
    users_items = Series(index=train.columns)
    items_users = Series(index=train.index)
    for u in train.columns:
        users_items[u] = train.index[train[u] != 0]
    for i in train.index:
        items_users[i] = train.columns[train.ix[i] != 0]
    print(items_users)

    #接下来开始随机游走——分为两步：随机走一步&随机停
    result = DataFrame(0.0, index= train.index, columns= train.columns)

    for u in train.columns:
        #print(users_items[u])
        for count in range(0, N):
            #todo:为什么没能完成抽样:1是数据格式，不能是列表，要是对象本身
            #todo：2是bug太多，行列的bug
            i = random.sample(list(users_items[u]), 1)[0]
            if filter_item:
                while i in users_items[u]:
                    while random.random() <= p:
                        iu = random.sample(list(items_users[i]), 1)[0]
                        i = random.sample(list(users_items[iu]), 1)[0]
            else:
                while random.random() <= p:
                    iu = random.sample(list(items_users[i]), 1)[0]
                    i = random.sample(list(users_items[iu]), 1)[0]
            if is_P:
                result[u][i] += 1 / N
            else:
                result[u][i] += 1

    #print(result)
    return result

