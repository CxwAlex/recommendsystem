#更多需要思考的是关于标签的这套系统如何设计
#输入数据：至少要有用户+商品+标签
#后台数据要有：1输入的原始记录，2标签对应的总数目，3用户所打的标签与对应的次数，4物品被打的标签以及对应的次数
#需要的功能：ETL（输入原始三元组，转换到所需格式——什么格式）；统计功能（离线or在线——存量与增量）
#计算相似度功能：
#用户的相似性：基于标签计算
#物品的相似性：基于标签计算
#标签的相似性：基于同一个物品计算&基于同一个用户计算
#todo:统一使用json的格式或者统一使用三元组

from pandas import Series,DataFrame
from book.cf2 import list2matrix, count_set
from collections import defaultdict
import random
import math
#需要以下功能函数：
#item_tag与tag_item互转
#todo:是用什么数据结构来表示比较好，是统一表示还是利用不同的表格来关联，利用不同的表格关联吧
#获取三元组数据的行和列
def get_user_item_tag(train):
    # etl模块，输入train，返回u，i，tag
    # todo:如何解决顺序问题
    u = set()
    i = set()
    t = set()
    for a in train:
        u.add(a[0])
        i.add(a[1])
        for tmp in a[2]:
            t.add(tmp)
    return u, i, t

def get_user_tags(train):
    # 获得user_tags矩阵
    users, items, tags = get_user_item_tag(train)
    result = DataFrame(0, index= tags, columns= users)
    for i in train:
        user = i[0]
        tags = i[2]
        for t in tags:
            result[user][t] += 1
    return result

def get_item_tags(train):
    # 获取item_tags矩阵
    users, items, tags = get_user_item_tag(train)
    result = DataFrame(0, index= tags, columns= items)
    for i in train:
        item = i[1]
        tags = i[2]
        for t in tags:
            result[item][t] += 1
    return result

def get_user_item(train):
    # 获取item_tags矩阵
    users, items, tags = get_user_item_tag(train)
    result = DataFrame(0, index= items, columns= users)
    for i in train:
        user = i[0]
        item = i[1]
        result[user][item] += 1
    return result

def count_tags(train):
    # 返回每个标签出现的次数
    tags = get_user_item_tag(train)[2]
    result =Series(0, index= tags)
    for i in train:
        tags = i[2]
        for t in tags:
            result[t] += 1
    return result


def matrix2list(train):
    return None

def item_and_tag_to_dataframe(train):
    # etl功能，将原始的list转换为dataframe
    train = list2matrix(train)
    return train

def item_and_tag_transfrom(train):
    # item和tag的相互转换
    result = defaultdict(list)
    if isinstance(train, DataFrame):
        for i in train.index:
            for j in train.columns[train.ix[i] != 0]:
                result[i].append(j)
    elif isinstance(train, dict):
        train = list2matrix(train)
        for i in train.index:
            for j in train.columns[train.ix[i] != 0]:
                result[i].append(j)

    return result


#根据user、item、tag为主键切分数据集
# 该数据集的作用是，测试给用户关于某一物品推荐的标签是否和其真正打的标签一致
# 输入的是原始数据集，返回的是分类好的训练集和测试集
# 注意，此处采用的是随机分类，所以只有在数据量比较大的情况下，才可以得到比较符合设定的比例
def SplitData(records):
    # todo：该部分上不可用
    # todo：需要原始格式的数据为user：item：tag格式
    # 假设此处使用的是三元组格式
    test = []
    train = []
    for record in records:
            if random.randint(1, 10) == 1:
                test.append(record)
            else:
                train.append(record)

    return train, test




#标签扩展：同一个物品的多个标签可能有一定的相似性
#需要标签的相似度
def recommend_tag():
    return None


#计算基于标签的物品余弦相似度
#此处假设不包含标签的次数
# todo:计算相似度时还要不要考虑打标签的次数
def item_similarity(item_tags, i=None, j=None):
    item_similarity = DataFrame(0.0, columns=item_tags.columns, index=item_tags.columns)
    for item_i in item_tags.columns:
        for item_j in item_tags.columns:
            count = 0
            if item_i == item_j:
                continue
            for tag in item_tags.index:
                if item_tags[item_i][tag] == 0 or item_tags[item_j][tag] == 0:
                    continue
                count += 1
            if count == 0:
                item_similarity[item_i][item_j] = 0
            else:
                item_similarity[item_i][item_j] = count / math.sqrt(count_set(item_tags[item_i]) * count_set(item_tags[item_j]))

    return item_similarity



#利用相似度度量计算推荐列表的多样性
# 如果推荐的物品相似度都很高，则说明多样性不强，反之，若相似度都不高，则说明多样性很高
# todo：这个评测在什么时候做，针对单个用户或者用户全体做等
# todo：暂时不能评测，因为推荐部分还没有完成——基于标签相似度的推荐
def Diversity(item_tags, recommend_items):
    ret = 0
    n = 0
    for i in recommend_items.keys():
        for j in recommend_items.keys():
            if i == j:
                continue
            ret += item_similarity(item_tags, i, j)
            n += 1
    #return 1 - ret / (n * 1.0)
    return None



#基于标签的推荐
#从 records 中统计出 user_tags 和 tag_items
#统计出user_tags和tag_items之后，就可以通过以下程序对用户进行个性化推荐
def Recommend(train, user):
    user_tags = get_user_tags(train)
    tag_items = get_item_tags(train).T
    user_items = get_user_item(train)
    recommend_items = defaultdict(int)
    tagged_items = user_items.index[user_items[user] != 0]

    for tag in user_tags.index[user_tags[user] != 0]:
        for item in tag_items.index[tag_items[tag] != 0]:
            if item in tagged_items:
                continue
            else:
                recommend_items[item] += user_tags[user][tag] * tag_items[tag][item]
    return recommend_items



#给用户推荐标签
#todo:此处尚没有决定带有标签的数据集的形式，因此暂时不测试

#给用户推荐整个系统里最热门的标签
def RecommendPopularTags(tags, N=1):
    return tags.sort_values(ascending=False).index.tolist()[0:N]


#给用户推荐物品i上最热门的标签
def RecommendItemPopularTags(item_tags, item=None, N=1):
    if not item:
        return None
    return item_tags[item].sort_values(ascending=False).index.tolist()[0:N]


#给用户推荐自己最经常会用的标签
def RecommendUserPopularTags(user_tags, user=None, N=1):
    if not user:
        return None
    return user_tags[user].sort_values(ascending=False).index.tolist()[0:N]

#结合上述两种方式
#alpha是指用户自己经常打的标签的权重
def RecommendHybridPopularTags(user,item, user_tags, item_tags, alpha = 0.3, N=1):
    # 此处假设两者传来的标签一致
    ret = Series(0.0, index= item_tags.index)
    max_user_tag_weight = user_tags[user].max()
    for tag in user_tags[user].index:
        ret[tag] = (1 - alpha) * user_tags[user][tag] / max_user_tag_weight
    max_item_tag_weight = item_tags[item].max()
    for tag in item_tags[item].index:
        ret[tag] += alpha * item_tags[item][tag] / max_item_tag_weight

    return ret.sort_values(ascending=False).index.tolist()[0:N]