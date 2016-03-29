import os, sys
import json
import flask
from flask.ext.security import (Security, MongoEngineUserDatastore,
                                UserMixin, RoleMixin, login_required)
# Set pythonpath (for settings)
#this_dir = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(this_dir)

# Initiate app
app = flask.Flask("Golden Sixpacks Web Interface")
app.config.from_object('goldensixpacks.settings')

# Read models and plug the database connection object into the app
import goldensixpacks.models
goldensixpacks.models.db.init_app(app)

# Setup Flask-Security
from models import User, Role
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# award data (nominations)
with open("award_data.json") as award_data_file:
    award_data = json.load(award_data_file)

# Load the views
import goldensixpacks.views

