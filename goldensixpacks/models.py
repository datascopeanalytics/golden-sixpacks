from flask.ext.security import UserMixin, RoleMixin
from flask.ext.mongoengine import MongoEngine

# Initiate a database connection object
db = MongoEngine()

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    name = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])

# class Category(db.Document)

    
# class Vote(db.Document):
#     voter_hash = db.StringField(max_length=255)
#     category
