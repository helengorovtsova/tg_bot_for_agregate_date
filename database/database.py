from pymongo import MongoClient
from mongoengine import connect

# Create a connection to MongoDB
client = MongoClient('localhost', 27017)

db = client['my_database']

collection = db['sample_collection']

# Connect to MongoDB using the mongoengine library
connect('my_database', host='localhost', port=27017)
