import flask
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.mongoengine import MongoEngine


# Initiate a database connection object
db = MongoEngine()

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=None)
    def __str__(self):
        return self.name
    
class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    def __str__(self):
        return self.email

class Category(db.Document):
    name = db.StringField(max_length=255)
    description = db.StringField(max_length=None)
    def __str__(self):
        return self.name
    
class Nomination(db.Document):
    category = db.ReferenceField(Category)
    nominee = db.StringField(max_length=255)
    nominator = db.StringField(max_length=255)
    what_for = db.StringField(max_length=None)
    def __str__(self):
        return "%s-->%s [by %s]" % (self.nominee,
                                    self.category,
                                    self.nominator)

    
class Vote(db.Document):
    vote_id = db.StringField(max_length=255, unique=True)
    voter_hash = db.StringField(max_length=255)
    category = db.ReferenceField(Category)
    voted_for = db.StringField(max_length=255)
    def __str__(self):
        return "%s-->%s for %s" % (self.voter_hash,
                                    self.voted_for,
                                    self.category)


    
