import flask
from flask.ext.security import Security, MongoEngineUserDatastore

# Initiate app
app = flask.Flask(__name__)
app.config.from_object('goldensixpacks.settings')

# Read models and plug the database connection object into the app
from goldensixpacks.models import db, User, Role
db.init_app(app)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Load the views
import goldensixpacks.views

