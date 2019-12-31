import jieba
import jieba.analyse
from hanziconv import HanziConv
import nltk
from pymongo import MongoClient

# MongoDB connection info
hostname = '52.54.130.90'
port = 27017
username = 'admin'
password = 'admin'
databaseName = 'admin'

client = MongoClient(hostname, port)
db = client[databaseName]
db.authenticate(username, password)

db = client['FinalProject']
mycol = db["20200101"]

post = []
postID = []

for x in mycol.find({}, {"_id": 1, "Post": 1}):
    post.append(x.get('Post'))
    postID.append(x.get('_id'))

# testTrainSeg = []
#
# for i in range(len(post)):
#     testTrainSeg.append([' '.join(list(jieba.cut(post[i], cut_all=False)))])
#     # testTrainSeg.append(list(jieba.cut(testTrainTrans[i], cut_all=False)))
#
# print(testTrainSeg)

keywords = []

for i in range(len(post)):
    keyword = jieba.analyse.extract_tags(post[i])

    if len(keyword) != 0:
        keywords.append(keyword[0])
    else:
        keywords.append("???")

for n in range(len(postID)):
    myQuery = {"_id": postID[n]}
    newValues = {"$set": {"Keyword": keywords[n]}}

    mycol.update_one(myQuery, newValues)


# abc = nltk.text.Text(jieba.analyse.extract_tags(post[i]))

# print(abc)
print(keywords)
print(postID)

# keyword.concordance('憂鬱')
