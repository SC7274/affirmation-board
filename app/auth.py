# filepath: /e:/2025/Affirmation_Board/affirmation-board/app/auth.py
from flask import Blueprint, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()

google = oauth.register(
    'google',
    client_id='your-google-client-id',
    client_secret='your-google-client-secret',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/auth/authorized',
    client_kwargs={'scope': 'email profile'}
)

@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('main.index'))

@auth_bp.route('/login/authorized')
def authorized():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    session['user'] = user_info
    return redirect(url_for('main.index'))
    