import flask

app = flask.Flask("Golden Sixpacks Web Interface")

@app.route("/")
def home():
    return flask.render_template(
        "home.html"
    )

if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
    )
    app.run(host='0.0.0.0')


