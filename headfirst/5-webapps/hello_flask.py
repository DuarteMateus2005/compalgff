from flask import Flask

app = Flask(__name__)

@app.route("/")

def hello() -> str:
    return "Óla fofinha gosto muito de tiiiiiiiiiiiiiiiii"

app.run()