from flask import Flask
app = Flask(__name__)

@app.route("/books/<book_id>")
def abook(book_id):
    return "I think you'll enjoy {}".format(book_id)
