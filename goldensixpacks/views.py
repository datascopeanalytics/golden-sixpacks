import json
from collections import defaultdict

import flask
from flask.ext.security import login_required
from flask_admin.contrib.mongoengine import ModelView as AdminModelView
from flask_admin import helpers as admin_helpers
from flask_security import current_user

from goldensixpacks import app, admin, security, user_datastore
from goldensixpacks.models import User, Role, Category, Nomination, Vote

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

    # User roles
    user_datastore.find_or_create_role(name='superuser',
                       description='runner of golden sixpack awards')
    user_datastore.find_or_create_role(name='voter',
                       description='a peer reviewer')

    # Initial superuser
    if not user_datastore.user_model.objects(email='datascope',
                                             password='datascope'):
        user_datastore.create_user(email='datascope',
                                   password='datascope',
                                   roles=['superuser', 'voter'])

    # Categories
    def ensure_category(name, desc):
        if not Category.objects(name=name):
            Category(name=name, description=desc).save()
    ensure_category("The Collaborator", ("is awesome to work with. They may "
                                      "have amazing brainstorming skills, "
                                      "they may always help right when needed, "
                                      "they may always be trusted to do things "
                                      "on their plate well, it may be tons of "
                                      "fun to work with them. In one or many "
                                      "ways, they are your favorite person to "
                                      "collaborate with."))
    ensure_category("The Closer", ("is the bringer of new clients and projects, "
                                   "closer of sales, signer of contracts, bringer "
                                   "of revenue to Datascope."))
        
    
@app.route("/")
def home():
    return flask.render_template(
        "home.html"
    )

@app.route('/vote/<category_no>')
@login_required
def vote(category_no):
    all_categories = list(Category.objects.order_by('name'))
    category_no = int(category_no)
    if category_no >= len(all_categories):
        return "DONE" # redirect to finished page

    category = all_categories[category_no]
    nominations = Nomination.objects(category=category)
    grouped_nominations = defaultdict(list)
    for nomination in nominations:
        grouped_nominations[nomination.nominee].append(nomination)
    app.logger.info(grouped_nominations)
    return flask.render_template('vote.html',
                                 category_no = category_no,
                                 category=category,
                                 grouped_nominations=grouped_nominations)

@app.route('/save_vote')
def save_vote():
    vote = request.args.get('field')
    return vote 

