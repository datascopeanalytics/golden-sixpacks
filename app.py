import json

import flask


app = flask.Flask("Golden Sixpacks Web Interface")

with open("award_data.json") as award_data_file:
    award_data = json.load(award_data_file)

@app.route("/")
def home():
    return flask.render_template(
        "home.html"
    )

@app.route('/vote/<award_id>')
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

