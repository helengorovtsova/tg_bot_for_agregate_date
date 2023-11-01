from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['my_database']

collection = db['sample_collection']

for document in collection.find():
    pass
