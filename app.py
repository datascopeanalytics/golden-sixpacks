import json
import flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import (Security, MongoEngineUserDatastore,
                                UserMixin, RoleMixin, login_required)

app = flask.Flask("Golden Sixpacks Web Interface")
app.config.from_object('settings')

# Create database connection object
db = MongoEngine(app)

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.Document, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    name = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    confirmed_at = db.DateTimeField()
    roles = db.ListField(db.ReferenceField(Role), default=[])


# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# award data (nominations)
with open("award_data.json") as award_data_file:
    award_data = json.load(award_data_file)


# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(email='irmak.sirer@datascopeanalytics.com',
                               password='password',
                               name='Irmak')

    
@app.route("/")
def home():
    return flask.render_template(
        "home.html"
    )

@app.route('/vote/<award_id>')
@login_required
def vote(award_id):
    award_id = int(award_id)
    if award_id >= len(award_data):
        return "DONE"
    else:
        return flask.render_template('vote.html',
                                     data=award_data[award_id])

@app.route('/save_vote')
def save_vote():
    vote = request.args.get('field')
    return vote 


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
    )
    app.run(host='0.0.0.0')

