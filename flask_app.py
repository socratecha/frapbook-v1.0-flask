from flask import Flask
app = Flask(__name__)

@app.route("/one")
def favorite():
    return "Thank you!"

@app.route("/one/triceratops")
@app.route("/")
def hello():
    return "Hello World!"
