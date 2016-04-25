import json

import flask
from flask.ext.security import login_required

from goldensixpacks import app, security, user_datastore
from goldensixpacks.models import User, Role, Category, Nomination, Vote

# Award data (nominations)
with open("award_data.json") as award_data_file:
    award_data = json.load(award_data_file)

# Create a user to test with
@app.before_first_request
def create_test_data():
    user_datastore.find_or_create_role(name='admin',
                               description='runner of golden sixpack awards')
    user_datastore.find_or_create_role(name='voter',
                               description='participator in golden sixpack voting')

    # Create users
    User.objects.delete() # FRESH START!

    user_datastore.create_user(email='irmak',
                               password='',
                               roles=['admin', 'voter'])
    user_datastore.create_user(email='mike',
                               password='',
                               roles=['voter'])
    
    # Create token data
    category = Category(name="The Collaborator",
                        description=("is awesome to work with. They may "
                                     "have amazing brainstorming skills, "
                                     "they may always help right when needed, "
                                     "they may always be trusted to do things "
                                     "on their plate well, it may be tons of "
                                     "fun to work with them. In one or many "
                                     "ways, they are your favorite person to "
                                     "collaborate with."))
    category.save()

    Nomination(category=category,
               nominee="Bo")
    

    
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

