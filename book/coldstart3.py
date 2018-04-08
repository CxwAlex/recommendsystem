#使用关键词-物品倒排表计算物品相似度
function CalculateSimilarity(entity-items)
    w = dict()
    ni = dict()
    for e,items in entity_items.items():
        for i,wie in items.items():
            addToVec(ni, i, wie * wie)
            for j,wje in items.items():
                addToMat(w, i, j, wie, wje)
    for i, relate_items in w.items():
        relate_items = {x:y/math.sqrt(ni[i] * ni[x]) for x,y in relate_items.items()}





