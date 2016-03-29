from flask.ext.security import UserMixin, RoleMixin

# This is using the Flask Application Factory pattern
from flask.ext.mongoengine import MongoEngine
db = MongoEngine(app)

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
