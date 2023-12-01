from mongoengine import Document, StringField, IntField

class User(Document):
    telegramId = StringField(required=True,unique=True)
    name = StringField(required=True)
    gender = StringField(required=True)
    genderOfInterest = StringField(required=True)
    age = IntField(required=True)
    location = StringField(required=True)
    image = StringField()
