#此章主要用来补充一些不需要用到推荐逻辑的推荐引擎
#todo:这里的过滤怎么处理
from book.cf2 import count_set
from pandas import Series, DataFrame

#随机推荐引擎


#最热门推荐
def most_popilarity_recommend(dataframe, N= None):
    result = Series(index= dataframe.index)
    for i in dataframe.index:
        result[i] = count_set(dataframe.ix[i])

    if N:
        result = result.sort_values(ascending=False).index[0:N]
    else:
        result = result.sort_values(ascending=False).index

    return result

#todo:最近最热门如何实现：是在数据选入阶段只选择最近24小时，还是选择之后在进行处理
#最近最热门推荐算法
def RecentPopularity(records, alpha, T):
    ret = dict()
    for user,item,tm in records:
        if tm >= T:
            continue
        addToDict(ret, item, 1 / (1.0 + alpha * (T - tm)))
    return ret

#出于商业目的推荐