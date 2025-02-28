from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from random import randint
import os

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth(app)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    oauth_token = db.Column(db.String(256), nullable=True)

google = oauth.remote_app(
    'google',
    consumer_key=app.config['OAUTH_CREDENTIALS']['google']['id'],
    consumer_secret=app.config['OAUTH_CREDENTIALS']['google']['secret'],
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    quotes = Quote.query.all()
    randomNumber = randint(0, len(quotes) - 1)
    quote = quotes[randomNumber].text
    return render_template('affirmation.html', quote=quote)

@app.route('/', methods=['POST'])
def my_form_post():
    message = request.form['user_quote']
    new_quote = Quote(text=message)
    db.session.add(new_quote)
    db.session.commit()

    quotes = Quote.query.all()
    randomNumber = randint(0, len(quotes) - 1)
    quote = quotes[randomNumber].text
    return render_template('affirmation.html', quote=quote)

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token')
    session.pop('user')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    user_data = user_info.data
    user = User.query.filter_by(email=user_data['email']).first()
    if user is None:
        user = User(username=user_data['name'], email=user_data['email'])
        db.session.add(user)
        db.session.commit()
    session['user'] = user_data
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    