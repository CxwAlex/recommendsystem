#社会化推荐： familiarity 存储了每个用户最熟悉的 K 个好友和他们的熟悉程度，
#similarity 存储了和每个用户兴趣最相关的 K 好友和他们的兴趣相似度。
#train 记录了每个用户的行为记录，其中 train[u] 记录了用户 u 喜欢的物品列表
def Recommend(uid, familiarity, similarity, train):
    rank = dict()
    interacted_items = train[uid]
    for fid,fw in familiarity[uid]:
        for item,pw in train[fid]:
            # if user has already know the item
            # do not recommend it
            if item in interacted_items:
                continue
            addToDict(rank, item, fw * pw)
    for vid,sw in similarity[uid]:
        for item,pw in train[vid]:
            if item in interacted_items:
                continue
            addToDict(rank, item, sw * pw)
    return rank

#无向社交网络，根据共同好友比例计算相似度
def FriendSuggestion(user, G, GT):
    suggestions = dict()
    friends = G[user]
    for fid in G[user]:
        for ffid in GT[fid]:
            if ffid in friends:
                continue
            if ffid not in suggestions:
                suggestions[ffid] = 0
            suggestions[ffid] += 1
    suggestions = {x: y / math.sqrt(len(G[user]) * len(G[x]) for x,y in suggestions}

#有向社交网络中的相似度
def FriendSuggestion(user, G, GT):
    suggestions = dict()
    for fid in GT[user]:
        for ffid in G[fid]:
            if ffid in friends:
                continue
            if ffid not in suggestions:
                suggestions[ffid] = 0
            suggestions[ffid] += 1
    suggestions = {x: y / math.sqrt(len(GT[user]) * len(GT[x]) for x, y in suggestions}

#有向网络中惩罚名人后的相似度

def FriendSuggestion(user, G, GT):
    suggestions = dict()
    for fid in GT[user]:
        for ffid in G[fid]:
            if ffid in friends:
                continue
            if ffid not in suggestions:
                suggestions[ffid] = 0
            suggestions[ffid] += 1
    suggestions = {x: y / math.sqrt(len(GT[user]) * len(GT[x]) for x, y in suggestions}




