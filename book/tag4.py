#计算基于标签的物品余弦相似度
def CosineSim(item_tags, i, j):
    ret = 0
    for b,wib in item_tags[i].items():
        if b in item_tags[j]:
            ret += wib * item_tags[j][b]
    ni = 0
    nj = 0
    for b, w in item_tags[i].items():
        ni += w * w
    for b, w in item_tags[j].items():
        nj += w * w
    if ret == 0:
        return 0
    return ret / math.sqrt(ni * nj)

#利用相似度度量计算推荐列表的多样性
def Diversity(item_tags, recommend_items):
    ret = 0
    n = 0
    for i in recommend_items.keys():
        for j in recommend_items.keys():
            if i == j:
                continue
            ret += CosineSim(item_tags, i, j)
            n += 1
    return ret / (n * 1.0)

#基于标签的推荐
#用 records 存储标签数据的三元组，其中 records[i] = [user, item, tag] ;
#用 user_tags  存储 n u,b ，其中 user_tags[u][b] =  n u,b ;
#用 tag_items 存储 n b,i ，其中 tag_items[b][i] = n b,i 。

#从 records 中统计出 user_tags 和 tag_items
def InitStat(records):
    user_tags = dict()
    tag_items = dict()
    user_items = dict()
    for user, item, tag in records.items():
        addValueToMat(user_tags, user, tag, 1)
        addValueToMat(tag_items, tag, item, 1)
        addValueToMat(user_items, user, item, 1)

#统计出user_tags和tag_items之后，就可以通过以下程序对用户进行个性化推荐
def Recommend(user):
    recommend_items = dict()
    tagged_items = user_items[user]
    for tag, wut in user_tags[user].items():
        for item, wti in tag_items[tag].items():
            #if items have been tagged, do not recommend them
            if item in tagged_items:
                continue
            if item not in recommend_items:
                recommend_items[item] = wut * wti
            else:
                recommend_items[item] += wut * wti
    return recommend_items

#给用户推荐标签

#给用户推荐整个系统里最热门的标签
def RecommendPopularTags(user,item, tags, N):
    return sorted(tags.items(), key=itemgetter(1), reverse=True)[0:N]

#给用户推荐物品i上最热门的标签
def RecommendItemPopularTags(user,item, item_tags, N):
    return sorted(item_tags[item].items(), key=itemgetter(1), reverse=True)[0:N]

#给用户推荐自己最经常会用的标签
def RecommendUserPopularTags(user,item, user_tags, N):
    return sorted(user_tags[user].items(), key=itemgetter(1), reverse=True)[0:N]

#结合上述两种方式
def RecommendHybridPopularTags(user,item, user_tags, item_tags, alpha, N):
    max_user_tag_weight = max(user_tags[user].values())
    for tag, weight in user_tags[user].items():
        ret[tag] = (1 – alpha) * weight / max_user_tag_weight

    max_item_tag_weight = max(item_tags[item].values())
    for tag, weight in item_tags[item].items():
        if tag not in ret:
            ret[tag] = alpha * weight / max_item_tag_weight
        else:
            ret[tag] += alpha * weight / max_item_tag_weight
    return sorted(ret[user].items(), key=itemgetter(1), reverse=True)[0:N]

#根据user、item、tag为主键切分数据集
def SplitData(records, train, test):
    for user,item, tag in records:
        if random.randint(1,10) == 1:
            test.append([user,item,tag])
        else:
            train.append([user,item,tag])
    return [train, test]




