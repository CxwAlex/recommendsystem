#对物品内容相似度的推荐
#具体的修改以及测试，需要机器学习先识别出物体的内容，所以此处从略


#对两两物品计算余弦相似度
# 计算文档D中所有关键词两两之间的相似性
def CalculateSimilarity_D(D)
    for di in D:
        for dj in D:
            w[i][j] = CosineSimilarity(di, dj)
    return w

#使用关键词-物品倒排表计算物品相似度
#进而进行基于物品内容的计算（此处简化为标题）
def CalculateSimilarity(train):
    #首先进行关键字的提取，生成每个物品的内容特征

    #然后统计关键字，基于关键字建立关键字和物品的倒排表

    #根据倒排表生成物品相似度——同基于用户来生成

    w = dict()
    ni = dict()
    for e,items in entity_items.items():
        for i,wie in items.items():
            addToVec(ni, i, wie * wie)
            for j,wje in items.items():
                addToMat(w, i, j, wie, wje)
    for i, relate_items in w.items():
        relate_items = {x:y/math.sqrt(ni[i] * ni[x]) for x,y in relate_items.items()}

    return None



