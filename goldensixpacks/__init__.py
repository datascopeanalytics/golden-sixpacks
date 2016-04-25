import flask
from flask_admin import Admin
from flask.ext.security import Security, MongoEngineUserDatastore


# Initiate app
app = flask.Flask(__name__)
app.config.from_object('goldensixpacks.settings')


# Customize the login form for the admin app

# Initiate the admin app
admin = Admin(app,
              name='Golden Sixpacks',
              base_template='secure_admin.html',
              template_mode='bootstrap3')

# Read models and plug the database connection object into the app
from goldensixpacks.models import db, User, Role

db.init_app(app)

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Load the views
import goldensixpacks.views

