from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection info
hostname = '52.54.130.90'
port = 27017
username = 'admin'
password = 'admin'
databaseName = 'admin'

# connect with authentication
client = MongoClient(hostname, port)
db = client[databaseName]
db.authenticate(username, password)

db = client['FinalProject']
mycol = db["20200101"]

# test = []
#
# x = mycol.find_one()
# print(x)

for x in mycol.find():
    print(x)

# test1 = []
#
# for x in mycol.find({"_id": test[0]}):
#     test1.append(x)


# print(test)

# myquery = { "": { "$regex": "^S" } }
# newvalues = { "$set": { "Keyword": "Minnie" } }
#
# x = mycol.update_many(myquery, newvalues)
#
# print(x.modified_count, "documents updated.")

