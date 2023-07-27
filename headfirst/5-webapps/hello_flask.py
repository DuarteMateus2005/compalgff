from flask import flask

app = Flask(__name__)

@app.route("/")

def hello() -> str:
    return "Hello world from Flask!"

app.run()