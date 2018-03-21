#推荐模块的大体工作流程
def RecommendationCore(features, related_table):
    ret = dict()
    for fid, fweight in features.items()
        for item, sim in related_table[fid].items():
            ret[item].weight += sim * fweight
            ret[item].reason[fid] = sim * fweight
    return ret

#根据推荐理由增加推荐多样性（每次拿出一个结果，若已经使用过，则对其降权）
def ReasonDiversity(recommendations):
    reasons = set()
    for i in recommendations:
        if i.reason in reasons:
            i.weight /= 2
        reasons.add(i.reason)
    recommendations = sortByWeight(recommendations)

