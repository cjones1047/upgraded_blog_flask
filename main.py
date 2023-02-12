from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)

all_posts_response = requests.get("https://api.npoint.io/c0d14f8f998f191dfe71")
all_posts_response.raise_for_status()
all_posts_json = all_posts_response.json()


@app.context_processor
def add_imports():
    return dict(datetime=datetime)


@app.route('/')
def home():
    return render_template("index.html", all_posts_json=all_posts_json)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
