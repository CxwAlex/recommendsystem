
#实际上的多引擎并不单单只是指算法上的多引擎，更多的是指在业务上的：
#比如专门负责冷启动的，专门负责重点广告业务的等，即常见的浏览器中其他文章+广告的模式

#推荐系统核心模块，处理的是特征维度，而不仅仅是简单的行为、矩阵、图
#对单一用户的推荐+推荐理由
def RecommendationCore(features, related_table):
    ret = dict()
    for fid, fweight in features.items():
        for item, sim in related_table[fid].items():
            ret[item].weight += sim * fweight
            ret[item].reason[fid] = sim * fweight
    return ret

def sortByWeight(recommendations):
    return None

#根据推荐理由增加推荐多样性（每次拿出一个结果，若已经使用过，则对其降权）
def ReasonDiversity(recommendations):
    reasons = set()
    for i in recommendations:
        if i.reason in reasons:
            i.weight /= 2
        reasons.add(i.reason)
    recommendations = sortByWeight(recommendations)

