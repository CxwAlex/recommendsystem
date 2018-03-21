#计算类类平均值（用户分类对物品分类的平均值）
def PredictAll(records, user_cluster, item_cluster):
    total = dict()
    count = dict()
    for r in records:
        if r.test != 0:
            continue
        gu = user_cluster.GetGroup(r.user)
        gi = item_cluster.GetGroup(r.item)
        basic.AddToMat(total, gu, gi, r.vote)
        basic.AddToMat(count, gu, gi, 1)
    for r in records:
        gu = user_cluster.GetGroup(r.user)
        gi = item_cluster.GetGroup(r.item)
        average = total[gu][gi] / (1.0 * count[gu][gi] + 1.0)
        r.predict = average

#下面的 Python 代码给出了不同的 user_cluster 和 item_cluster 定义方式
class Cluster:
    def __init__(self,records):
        self.group = dict()

    def GetGroup(self, i):
        return 0

class IdCluster(Cluster):
    def __init__(self, records):
        Cluster.__init__(self, records)

    def GetGroup(self, i):
        return i

class UserActivityCluster(Cluster):
    def __init__(self, records):
        Cluster.__init__(self, records)
        activity = dict()
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(activity, r.user, 1)
        k = 0
        for user, n in sorted(activity.items(), key=itemgetter(1), reverse=False):
            c = int((k * 5) / (1.0 * len(activity)))
            self.group[user] = c
            k += 1

    def GetGroup(self, uid):
        if uid not in self.group:
            return -1
        else:
            return self.group[uid]

class ItemPopularityCluster(Cluster):
    def __init__(self, records):
        Cluster.__init__(self, records)
        popularity = dict()
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(popularity, r.item, 1)
        k = 0
        for item, n in sorted(popularity.items(), key=itemgetter(1), reverse=False):
            c = int((k * 5) / (1.0 * len(popularity)))
            self.group[item] = c
            k += 1

    def GetGroup(self, item):
        if item not in self.group:
            return -1
        else:
            return self.group[item]

class UserVoteCluster(Cluster):
    def __init__(self, records):
        Cluster.__init__(self, records)
        vote = dict()
        count = dict()
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(vote, r.user, r.vote)
            basic.AddToDict(count, r.user, 1)
        k = 0
        for user, v in vote.items():
            ave = v / (count[user] * 1.0)
            c = int(ave * 2)
            self.group[user] = c

    def GetGroup(self, uid):
        if uid not in self.group:
            return -1
        else:
            return self.group[uid]

class ItemVoteCluster(Cluster):
    def __init__(self, records):
        Cluster.__init__(self, records)
        vote = dict()
        count = dict()
        for r in records:
            if r.test != 0:
                continue
            basic.AddToDict(vote, r.item, r.vote)
            basic.AddToDict(count, r.item, 1)
        k = 0
        for item, v in vote.items():
            ave = v / (count[item] * 1.0)
            c = int(ave * 2)
            self.group[item] = c

    def GetGroup(self, item):
        if item not in self.group:
            return -1
        else:
            return self.group[item]

#使用基于邻域的方法计算用户相似度和最终的预测函数
def UserSimilarity(records):
    item_users = dict()
    ave_vote = dict()
    activity = dict()
    for r in records:
        addToMat(item_users, r.item, r.user, r.value)
        addToVec(ave_vote, r.user, r.value)
        addToVec(activity, r.user, 1)
    ave_vote = {x:y/activity[x] for x,y in ave_vote.items()}
    nu = dict()
    W = dict()
    for i,ri in item_users.items():
        for u,rui in ri.items():
            addToVec(nu, u, (rui - ave_vote[u])*(rui - ave_vote[u]))
            for v,rvi in ri.items():
                if u == v:
                    continue
                addToMat(W, u, v, (rui - ave_vote[u])*(rvi - ave_vote[v]))
    for u in W:
        W[u] = {x:y/math.sqrt(nu[x]*nu[u]) for x,y in W[u].items()}
    return W

def PredictAll(records, test, ave_vote, W, K):
    user_items = dict()
    for r in records:
        addToMat(user_items, r.user, r.item, r.value)
    for r in test:
        r.predict = 0
        norm = 0
        for v,wuv in sorted(W[r.user].items(), key=itemgetter(1), reverse=True)[0:K]:
            if r.item in user_items[v]:
                rvi = user_items[v][r.item]
                r.predict += wuv * (rvi - ave_vote[v])
                norm += abs(wuv)
        if norm > 0:
            r.predict /= norm
        r.predict += ave_vote[r.user]

#学习LFM模型的迭代过程
def LearningLFM(train, F, n, alpha, lambda):
    [p,q] = InitLFM(train, F)
    for step in range(0, n):
        for u,i,rui in train.items():
            pui = Predict(u, i, p, q)
            eui = rui - pui
            for f in range(0,F):
                p[u][k] += alpha * (q[i][k] * eui - lambda * p[u][k])
                q[i][k] += alpha * (p[u][k] * eui - lambda * q[i][k])
        alpha *= 0.9
    return list(p, q)

#促使化P,Q矩阵
def InitLFM(train, F):
    p = dict()
    q = dict()
    for u, i, rui in train.items():
        if u not in p:
            p[u] = [random.random() / math.sqrt(F) for x in range(0, F)]
        if i not in q:
            q[i] = [random.random() / math.sqrt(F) for x in range(0, F)]
    return list(p, q)

#预测用户u对物品i的评分
def Predict(u, i, p, q):
    return sum(p[u][f] * q[i][f] for f in range(0, len(p[u]))

#biasLFM_加入偏置项后的LFM

def LearningBiasLFM(train, F, n, alpha, lambda, mu):
    [bu, bi, p, q] = InitLFM(train, F)
    for step in range(0, n):
        for u, i, rui in train.items():
            pui = Predict(u, i, p, q, bu, bi, mu)
            eui = rui - pui
            bu[u] += alpha * (eui - lambda *bu[u])
            bi[i] += alpha * (eui - lambda *bi[i])
            for f in range(0, F):
                p[u][k] += alpha * (q[i][k] * eui - lambda *p[u][k])
                q[i][k] += alpha * (p[u][k] * eui - lambda *q[i][k])
        alpha *= 0.9
    return list(bu, bi, p, q)

#初始化bu，bi向量
def InitBiasLFM(train, F):
    p = dict()
    q = dict()
    bu = dict()
    bi = dict()
    for u, i, rui in train.items():
        bu[u] = 0
        bi[i] = 0
        if u not in p:
            p[u] = [random.random() / math.sqrt(F) for x in range(0, F)]
        if i not in q:
            q[i] = [random.random() / math.sqrt(F) for x in range(0, F)]
            return
list(p, q)

def Predict(u, i, p, q, bu, bi, mu):
    ret = mu + bu[u] + bi[i]
    ret += sum(p[u][f] * q[i][f] for f in range(0, len(p[u]))
    return ret

#SVD++，考虑邻域影响的LFM
def LearningBiasLFM(train_ui, F, n, alpha, lambda, mu):
    [bu, bi, p, q, y] = InitLFM(train, F)
    z = dict()
    for step in range(0, n):
        for u, items in train_ui.items():
            z[u] = p[u]
            ru = 1 / math.sqrt(1.0 * len(items))
            for i, rui in items items():
                for f in range(0, F):
                    z[u][f] += y[i][f] * ru
            sum = [0 for i in range(0, F)]
            for i, rui in items items():
                pui = Predict()
                eui = rui - pui
                bu[u] += alpha * (eui - lambda *bu[u])
                bi[i] += alpha * (eui - lambda *bi[i])
                for f in range(0, F):
                    sum[k] += q[i][k] * eui * ru
                    p[u][k] += alpha * (q[i][k] * eui - lambda *p[u][k])
                    q[i][k] += alpha * ((z[u][k] + p[u][k]) * eui - lambda *q[i][k])
            for i, rui in items items():
                for f in range(0, F):
                    y[i][f] += alpha * (sum[f] - lambda *y[i][f])
        alpha *= 0.9
    return list(bu, bi, p, q)

#利用平均值预测期进行级联融合
def Predict(train, test, alpha):
    total = dict()
    count = dict()
    for record in train:
        gu = GetUserGroup(record.user)
        gi = GetItemGroup(record.item)
        AddToMat(total, gu, gi, record.vote - record.predict)
        AddToMat(count, gu, gi, 1)
    for record in test:
        gu = GetUserGroup(record.user)
        gi = GetUserGroup(record.item)
        average = total[gu][gi] / (1.0 * count[gu][gi] + alpha)
        record.predict += average



