#cf2
'''
#以下皆是LFM模型中所使用的函数，尚未进行优化编写
#负样本采样——找出热门的但用户没有行为的物品
def RandomSelectNegativeSample(self, items):
    ret = dict()
    for i in items.keys():
        ret[i] = 1
    n = 0
    for i in range(0, len(items) * 3):
        item = items_pool[random.randint(0, len(items_pool) - 1)]
        if item in ret:
            continue
        ret[item] = 0
        n + = 1
        if n > len(items):
            break
    return ret


#随机梯度下降法学习参数
def LatentFactorModel(user_items, F, N, alpha, lambda):
    [P, Q] = InitModel(user_items, F)
    for step in range(0,N):
        for user, items in user_items.items():
            samples = RandSelectNegativeSamples(items)
            for item, rui in samples.items():
                eui = rui - Predict(user, item)
                for f in range(0, F):
                    P[user][f] += alpha * (eui * Q[item][f] - lambda * P[user][f])
                    Q[item][f] += alpha * (eui * P[user][f] - lambda * Q[item][f])
        alpha *= 0.9

    return alpha

def Recommend(user, P, Q):
    rank = dict()
    for f, puf in P[user].items():
        for i, qfi in Q[f].items():
            if i not in rank:
            rank[i] += puf * qfi
    return rank
'''


#social6
'''
#有向社交网络中的相似度
def FriendSuggestion_have_direction(user, G, GT):
    suggestions = dict()
    for fid in GT[user]:
        for ffid in G[fid]:
            if ffid in friends:
                continue
            if ffid not in suggestions:
                suggestions[ffid] = 0
            suggestions[ffid] += 1
    suggestions = {x: y / math.sqrt(len(GT[user]) * len(GT[x]) for x, y in suggestions}
'''

'''
def similarity_two_user(u, v, dataframe, filter):
    if u == v or dataframe[u][v] == 1:
        if filter:
            result = 0
        else:
            result = 1
    else:
        result = count_set(dataframe[u] & dataframe.ix[v]) / \
                            math.sqrt(1.0 * count_set(dataframe[u]) * count_set(dataframe.ix[v]))
    return result

#无向社交网络，根据共同好友比例计算相似度
#todo:此处的定义，相似度怎么算
#todo:是否要传递整个dataframe，这样会不会增加整个功能的开销
#todo：代码的简洁和整个工程的效率如何衡量
def FriendSuggestion_no_direction(dataframe, filter= True, user= None):
    if user:
        similarity = Series(0.0, index= dataframe.index)
        for v in dataframe.index:
            similarity[user][v] += similarity_two_user(user, v, dataframe, filter)
    else:
        similarity = DataFrame(0.0, index= dataframe.index, columns= dataframe.columns)
        for u in dataframe.columns:
            for v in dataframe.index:
                similarity[u][v] += similarity_two_user(user, v, dataframe, filter)
    print(similarity)
    return similarity



'''

#context5
#获取三元组的行和列
#unique算法
'''
    # 方法二
    u = []
    i = []
    ids = [1, 4, 3, 3, 4, 2, 3, 4, 5, 6, 1]
    news_ids = list(set(ids))
    news_ids.sort(ids.index)
    
    #方法三
    
    In [5]: ids = [1,4,3,3,4,2,3,4,5,6,1]

    In [6]: func = lambda x,y:x if y in x else x + [y]

    In [7]: reduce(func, [[], ] + ids)
    Out[7]: [1, 4, 3, 2, 5, 6]
    
'''
'''

    #此处时使用倒排方式，计算用户相似度
    for item in train.index:
        #todo:此处的全columns循环改写为只对value不为0的user循环
        #已经得到了倒排表——使用内建表达式，效率高
        users = train.columns[not pd.isnull(train.ix[item])]
        print(item, users)
        for u in users:
            for v in users:
                if u == v:
                    C[u][v] += 1
                    continue
                C[u][v] += 1 / math.log(1 + len(users))

'''
'''

def nan2zero(train):
    if isinstance(train, Series):
        result = Series(0,index=train.index)
        for i in train.index:
            if np.isnan(train[i]):
                continue
            else:
                result[i] = 1

    elif isinstance(train, DataFrame):
        result = DataFrame(0,index=train.index, columns=train.columns)
        for u in train.columns:
            for i in train.index:
                if np.isnan(train[u][i]):
                    continue
                else:
                    result[u][i] = 1
    return result


    def test_nan2zero(self):
        train = list2dataframe_time(raw_data)
        result = nan2zero(train)
        self.assertEqual(result[1][1], 1)
        self.assertEqual(result[6][1], 0)

'''
'''

#基于图的路径融合算法
def PathFusion(user, time,G,alpha)
    Q = []
    V = set()
    depth = dict()
    rank = dict()
    depth['u:' + user] = 0
    depth['ut:' + user + '_' + time] = 0
    rank ['u:' + user] = alpha
    rank ['ut:' + user + '_' + time] = 1 - alpha
    Q.append('u:' + user)
    Q.append('ut:' + user + '_' + time)
    while len(Q) > 0:
        v = Q.pop()
        if v in V:
            continue
        if depth[v] > 3:
            continue
        for v2,w in G[v].items():
            if v2 not in V:
                depth[v2] = depth[v] + 1
                Q.append(v2)
            rank[v2] = rank[v] * w
    return rank


'''