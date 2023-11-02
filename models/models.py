from mongoengine import Document, DateTimeField, IntField

class Salary(Document):
    dt = DateTimeField()
    value = IntField()

    meta = {
        'collection': 'sample_collection'
    }
