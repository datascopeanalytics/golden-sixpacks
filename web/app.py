import flask

app = flask.Flask("Golden Sixpacks Web Interface")

@app.route("/")
def home():
    return flask.render_template(
        "home.html"
    )


poll_data = {
    'question' : 'Who are you voting for in the category of The Collaborator?',
    'fields'   : ['Bo', 'Irmak', 'Mike', 'Dean', 'Brian', 'Vlad', 'Mollie', 'Michael']
    }

@app.route('/vote')
def vote():
    return flask.render_template('vote.html', data=poll_data)

@app.route('/save_vote')
def poll():
    vote = request.args.get('field')
    return vote 


if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
    )
    app.run(host='0.0.0.0')

