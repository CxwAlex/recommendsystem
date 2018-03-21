import math
import operator
#计算RMSE和MAE
def RMSE(records):
    '''
    print(sum([(rui-pui)*(rui-pui) for u,i,rui,pui in records]) )
    print(float(len(records)))
    print(math.sqrt(\
    sum([(rui-pui)*(rui-pui) for u,i,rui,pui in records]) / float(len(records))))
    '''
    return math.sqrt(\
    sum([(rui-pui)*(rui-pui) for u,i,rui,pui in records]) / float(len(records)))

def MAE(records):
    return sum([abs(rui-pui) for u,i,rui,pui in records]) / float(len(records))

#计算准确率和召回率
def PrecisionRecall(test, N):
    hit = 0
    n_recall = 0
    n_precision = 0
    for user, items, rank in test:
        hit += sum(map(lambda x, y: 1 if x == y else 0, items, rank))
        n_recall += len(items)
        n_precision += N
    return [hit / (1.0 * n_recall), hit / (1.0 * n_precision)]

    '''
def PrecisionRecall(test, N):
    #原始版本，rank表示recommend处理推荐之后的结果集
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
    print(p)
    print(sorted(p, key=operator.itemgetter(1)))
    for item, weight in sorted(p, key=operator.itemgetter(1)):
        G += (2 * j - n - 1) * weight
    return G / float(n - 1)
    '''