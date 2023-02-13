from flask import Flask, render_template, request
from datetime import datetime
import requests
import os
import dotenv
import smtplib

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


@app.route('/contact', methods=["GET", "POST"])
def contact():
    header_message = None
    if request.method == "GET":
        header_message = "Contact Me"
    elif request.method == "POST":
        dotenv.load_dotenv()
        sender_email = os.getenv("SENDER_EMAIL")
        sender_email_password = os.getenv("SENDER_EMAIL_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL")
        message = (f"Subject:Message from {request.form['name']}\n\n"
                   f"Sender's email: {request.form['email']}\n"
                   f"Sender's phone number: {request.form['phone']}\n\n"
                   "Message:\n"
                   f"{request.form['message']}")

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=sender_email, password=sender_email_password)
            connection.sendmail(from_addr=sender_email,
                                to_addrs=recipient_email,
                                msg=message.encode("utf-8"))

        header_message = "Successfully sent your message"

    return render_template("contact.html", header_message=header_message)


@app.route('/post/<int:post_id>')
def get_post(post_id):
    requested_post = None
    for post in all_posts_json:
        if post['id'] == post_id:
            requested_post = post
            break

    return render_template("post.html", requested_post=requested_post)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
