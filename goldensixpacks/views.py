import json
from collections import defaultdict, Counter
import hashlib
import random

import flask
from flask.ext.security import login_required, roles_required
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
            
class SecureAdminUserModelView(SecureAdminModelView):
    column_list = ('email', 'active', 'roles')

    
# Add admin views
admin.add_view(SecureAdminUserModelView(User))
admin.add_view(SecureAdminModelView(Category))
admin.add_view(SecureAdminModelView(Nomination))

# Only turn on for debugging
# admin.add_view(SecureAdminModelView(Vote))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )

# Helper functions
def hash_it_baby(msg):
    """Helper hasher to obscure usernames for votes in the database.
    Not intended to be an unbreakable, just putting a cloudy ice-glass
    in front, so seeing who woted for what is not as easy as one simple
    query in the database"""
    return hashlib.sha224(msg).hexdigest()


def get_codename():
    """Helper for generating a random codename to represent a voter
    in the admin interface. To protect voting privacy of our voters,
    we are using hashes to make it slightly more difficult to
    reveal/infer who voted for who. On the admin interface, however,
    instead of using a less human-friendly hash, we are representing
    voters with randomly generated codenames, which still obscures
    who they are but looks a bit better. The codename is always randomly
    generated and does not stay the same like the hash, since we don't
    need to use it to track anything.
    """
    codename = random.choice(['Black', 'Blue', 'Red', 'Brown', 'Gray',
                              'Green', 'Yellow', 'Purple', 'White',
                              'Orange', 'Pink'])
    codename += " " + random.choice(['Mamba', 'Raptor', 'Eagle',
                                     'Hawk', 'Sparrow', 'Snake', 'Mosquito',
                                     'Turkey', 'Opossum', 'Narwhal',
                                     'Seabass','Octopus', 'Jellyfish',
                                     'Armadillo', 'Lemur', 'Tiger',
                                     'Whale', 'Elephant','Turtle', 
                                     'Dragon', 'Horse', 'Donkey', 'Coyote',
                                     'Penguin', 'Fox', 'Mouse', 'Albatross',
                                     'Mammoth', 'Tiger', 'Bear', 'Weasel'])
    return codename



# For a freshly setup Golden Sixpacks, populate the database with
# the initial data, like superusers and default categories
@app.before_first_request
def create_initial_data():

    # User roles
    user_datastore.find_or_create_role(name='superuser',
                       description='runner of golden sixpack awards')
    user_datastore.find_or_create_role(name='voter',
                       description='a peer reviewer')

    # Initial superuser
    if not user_datastore.user_model.objects(email='dumbledore',
                                             password='hogwarts4eva'):
        user_datastore.create_user(email='dumbledore',
                                   password='hogwarts4eva',
                                   roles=['superuser'])

    # Categories
    def ensure_category(name, desc):
        if not Category.objects(name=name):
            Category(name=name, description=desc).save()
            
    ensure_category("The Closer", ("is the bringer of new clients and projects, "
                                   "closer of sales, signer of contracts, bringer "
                                   "of revenue to Datascope. The Closer goes beyond "
                                   "the call of duty to bring in more projects. The Closer may "
                                   "be naturally gifted at sales, or not so at all; but he/she "
                                   "puts tons of effort into trying to sign new projects."))
    ensure_category("The Executer", ("is the getter-doner of shit. The Executer "
                                     "puts a lot of effort to make sure a project does "
                                     "not fall behind, or if it is behind, the Executer brings it "
                                     "back to life. It may be coding, it may be writing a report, "
                                     "it may be preparing for a workshop. Whatever the "
                                     "avenue, The Executer gets it done through high quality hard work."))
    ensure_category("The Navigator", ("is a major contributor to our culture and business design. "
                                      "The Navigator thinks hard on how to improve Datascope and spends "
                                      "a lot of energy to apply these thoughts practically."))
    ensure_category("The Corresponder", ("goes out of his/her way to keep clients informed and happy, "
                                         "pushes hard to make sure projects stay/end on time, replies to emails "
                                         "fast and well, keeps initiating communication, works hard to help the project teams "
                                         "organize and fires them up, tries to put the seeds of a next/future"
                                         "project with the clients."))
    ensure_category("The Professor", ("is a trainer of self and colleagues. From code to statistics "
                                      "to design to communication, the Professor makes an effort to learn new "
                                      "things and teach their coworkers. He/she helps enhance Datascope's "
                                      "skills and capabilities."))
    ensure_category("The Collaborator", ("is awesome to work with. The Collaborator may always "
                                         "offer take stuff off your plate into his/hers right when you need a break, "
                                         "or put extra effort to be productive/constructive at brainstorms, "
                                         "or give v. useful feedback without you having to prompt for it, "
                                         "or may always be trusted to do things on their plate well, "
                                         "or may motivate you with a lot of energy, or may put a lot of effort "
                                         "to lowering your stress or boredom by cracking jokes. In one or "
                                         "many ways, the Collaborator tries hard to make it easy and fun "
                                         "to work with them."))
    # Other Categories
    # ensure_category("The Networker", ("builds relationships with future potential clients, colleagues, and the community. "
    #                                   "The Navigator spends a lot of time arranging coffee meetings, going to "
    #                                   "networking events, connecting with people."))
    # ensure_category("The Rockstar", ("contributes to Datascope's reputation, by giving talks, "
    #                                  "writing engaging blog posts, organizing meetups, making waves through "
    #                                  "high profile pro bono work, or in any way putting a lot of "
    #                                  "effort into expanding the image and influence of Datascope."))
    # ensure_category("The Maker", ("builds useful internal tools that help improve Datascope, or builds "
    #                               "public tools that align with the Datascope brand. The maker creates "
    #                               "things that are not part of a client project but improve Datascope."))
                    
    
@app.route("/")
def home():
    return flask.render_template(
        "home.html"
    )

@app.route('/vote/<category_no>')
@login_required
def vote(category_no):
    all_categories = Category.objects.order_by('name')
    category_no = int(category_no)
    if category_no >= len(all_categories):
        return flask.redirect(flask.url_for('thank_you'))
    category = all_categories[category_no]
    nominations = Nomination.objects(category=category)
    if not nominations:
        next_no = category_no + 1
        return flask.redirect(flask.url_for('vote',
                                            category_no=next_no))
    grouped_nominations = defaultdict(list)
    for nomination in nominations:
        grouped_nominations[nomination.nominee].append(nomination)
    return flask.render_template('vote.html',
                                 category_no = category_no,
                                 category=category,
                                 grouped_nominations=grouped_nominations)

@app.route('/save-vote/<category_no>', methods=['POST'])
@roles_required('voter')
def save_vote(category_no):
    category_name, voted_for = flask.request.form['cast_vote'].split("|||")
    category = Category.objects(name=category_name).first()
    voter = current_user
    voter_hash = hash_it_baby(voter.email)
    vote_id = hash_it_baby('%s%s' % (voter,category))
    vote = Vote.objects(vote_id=vote_id).first()
    if vote:
        vote.voter_hash=voter_hash
        vote.category=category
        vote.voted_for=voted_for
    else:
        vote = Vote(vote_id=vote_id,
                    voter_hash=voter_hash,
                    category=category,
                    voted_for=voted_for)
    vote.save()
    next_no = str(int(category_no)+1)
    return flask.redirect(flask.url_for('vote',
                                        category_no=next_no))


@app.route('/participation')
@roles_required('superuser')
def participation():
    votes = Vote.objects
    voter_participation = Counter()
    for vote in votes:
        voter_participation[vote.voter_hash] += 1
    codename_participation= []
    voter_counts = voter_participation.most_common(10000)
    for voter, count in voter_counts:
        codename_participation.append((get_codename(), count))
    n_voted = len(codename_participation)
    voter_role = Role.objects(name='voter').first()
    all_voters = User.objects(roles = voter_role)
    n_voters = len(all_voters)
    for voter in range(n_voters-n_voted):
        codename_participation.append((get_codename(), 0))
    return flask.render_template('participation.html',
                                 n_all = n_voters,
                                 n_voted = n_voted,
                                 codename_participation = codename_participation)


@app.route('/results')
@roles_required('superuser')
def results():
    winners = {}
    any_nominations = {}
    for category in Category.objects:
        nominations_exist = bool(Nomination.objects(category=category).first())
        any_nominations[category.name] = nominations_exist
        votes = Vote.objects(category=category)
        tally = Counter([v.voted_for for v in votes]).most_common()
        cat_winners = []
        if tally:
            top_nominee, top_count = tally.pop(0)
            cat_winners.append((top_nominee, top_count))
        while tally:
            next_nominee, next_count = tally.pop(0)
            if next_count == top_count:
                cat_winners.append((next_nominee, next_count))
            else:
                break
        winners[category.name] = cat_winners
    return flask.render_template('results.html',
                                 winners=winners,
                                 any_nominations=any_nominations)

@app.route('/done')
@roles_required('voter')
def thank_you():
    return flask.render_template('thank_you.html')


                          

