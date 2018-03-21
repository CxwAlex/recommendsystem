import math
#计算RMSE和MAE
def RMSE(records):
    return math.sqrt(\
    sum([(rui-pui)*(rui-pui) for u,i,rui,pui in records]) / float(len(records)))
def MAE(records):
    return sum([abs(rui-pui) for u,i,rui,pui in records]) / float(len(records))
'''
#计算准确率和召回率
def PrecisionRecall(test, N):
    hit = 0
    n_recall = 0
    n_precision = 0
    for user, items in test.items():
        rank = Recommend(user, N)
        hit += len(rank & items)
        n_recall += len(items)
        n_precision += N
    return [hit / (1.0 * n_recall), hit / (1.0 * n_precision)]

#计算基尼系数
def GiniIndex(p):
    j = 1
    n = len(p)
    G = 0
    for item, weight in sorted(p.items(), key=itemgetter(1)):
        G += (2 * j - n - 1) * weight
    return G / float(n - 1)
'''