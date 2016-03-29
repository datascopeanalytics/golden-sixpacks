import json
import flask
from flask.ext.security import (Security, MongoEngineUserDatastore,
                                UserMixin, RoleMixin, login_required)

app = flask.Flask("Golden Sixpacks Web Interface")
app.config.from_object('settings')

# Create database connection object
# This is using the Flask Application Factory pattern
from models import db
db.init_app(app)

# Setup Flask-Security
from models import User, Role
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# award data (nominations)
with open("award_data.json") as award_data_file:
    award_data = json.load(award_data_file)

# Create a user to test with
@app.before_first_request
def create_users():
    user_datastore.find_or_create_role(name='admin',
                               description='runner of golden sixpack awards')
    user_datastore.find_or_create_role(name='voter',
                               description='participator in golden sixpack voting')

    User.objects.delete() # FRESH START!

    user_datastore.create_user(name='Irmak',
                               password='',
                               roles=['admin', 'voter'])
    user_datastore.create_user(name='Mike',
                               password='',
                               roles=['voter'])

    
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
    app.run(host='0.0.0.0')

