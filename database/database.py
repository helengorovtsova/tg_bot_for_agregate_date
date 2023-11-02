from pymongo import MongoClient
from mongoengine import connect

client = MongoClient('localhost', 27017)

db = client['my_database']

collection = db['sample_collection']

connect('my_database', host='localhost', port=27017)
