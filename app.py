from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random
import tweepy
from dotenv import load_dotenv
import os

##The code below that was commented out required elevated access to the twitter API

# load_dotenv()

# CONSUMER_KEY = os.getenv('CONSUMER_KEY')
# CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
# ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
# ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
# auth.set_access_token(os.environ.get("ACCESS_TOKEN"), os.environ.get("ACCESS_TOKEN_SECRET"))

# api = tweepy.API(auth)

# tweets = api.user_timeline(screen_name='jing_burger', count=10)




#### RANDOM VIDEOS ###

videos = [
    {
        'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        'img': 'https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg'
    },
    {
        'url': 'https://www.youtube.com/watch?v=YudHcBIxlYw',
        'img': 'https://i.ytimg.com/vi/YudHcBIxlYw/hqdefault.jpg'
    },
    {
        'url': 'https://www.youtube.com/watch?v=HBz9pOZOS4k',
        'img': 'https://i.ytimg.com/vi/HBz9pOZOS4k/hqdefault.jpg'
    },
    {
        'url': 'https://www.youtube.com/watch?v=1WEAJ-DFkHE',
        'img': 'https://i.ytimg.com/vi/1WEAJ-DFkHE/hqdefault.jpg'
    },
]


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = 'password'

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text(1000))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['user']
        email = request.form['email']
        message = request.form['message']
        new_opinion = Message(name=name, email=email, message=message)
        db.session.add(new_opinion)
        db.session.commit()
        flash('Your opinion has been sent!', 'success')
   
    comments = Message.query.all()
    random_sh = random.sample(videos, 2)
    return render_template('index.html', comments=comments, what = random_sh)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['user']
    email = request.form['email']
    message = request.form['message']
    new_opinion = Message(name=name, email=email, message=message)
    db.session.add(new_opinion)
    try:
        db.session.commit()
        flash('Your opinion has been sent!', 'success')
    except Exception as e:
        flash('An error occurred: ' + str(e), 'danger')
    return redirect(url_for('index'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/messages')
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)

@app.route('/messages/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted!', 'success')
    else:
        flash('Message not found!', 'danger')
    return redirect(url_for('messages'))


#Required elevated access to twitter API 
# @app.route('/tweets/<username>')
# def get_tweets(username):
#     tweets = api.user_timeline(screen_name=username, count=10)
#     return render_template('index.html', tweets=tweets)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

