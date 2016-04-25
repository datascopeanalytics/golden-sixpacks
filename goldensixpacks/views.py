import json

import flask
from flask.ext.security import login_required
from flask_admin.contrib.mongoengine import ModelView as AdminModelView
from flask_admin import helpers as admin_helpers
from flask_security import current_user

from goldensixpacks import app, admin, security, user_datastore
from goldensixpacks.models import User, Role, Category, Nomination, Vote

# Award data (nominations)
with open("award_data.json") as award_data_file:
    award_data = json.load(award_data_file)

# Create customized admin model view class
class SecureAdminModelView(AdminModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        
        if current_user.has_role('superuser'):
            return True

        return False
    
    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect 
        users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                flask.abort(403)
            else:
                app.logger.info('REDIRECT')
                # login
                return flask.redirect(flask.url_for('security.login',
                                                    next=flask.request.url))
            
            
    
# Add admin views
admin.add_view(SecureAdminModelView(User))
admin.add_view(SecureAdminModelView(Category))
admin.add_view(SecureAdminModelView(Nomination))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )
    
    
# Create a user to test with
@app.before_first_request
def create_initial_data():
    user_datastore.find_or_create_role(name='superuser',
                       description='runner of golden sixpack awards')
    user_datastore.find_or_create_role(name='voter',
                       description='a peer reviewer')

    # Create users
    User.objects.delete() # FRESH START AT APP START!

    user_datastore.create_user(email='datascope',
                               password='datascope',
                               roles=['superuser', 'voter'])
    
    
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

