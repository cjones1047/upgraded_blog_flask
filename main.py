from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.context_processor
def add_imports():
    return dict(datetime=datetime)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
