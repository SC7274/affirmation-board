from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app import db, oauth
from app.models import Quote, User
from random import choice

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_quote = request.form['user_quote']
        user_id = session.get('user_id')
        if user_id:
            new_quote = Quote(text=user_quote, user_id=user_id)
            db.session.add(new_quote)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False})
    quotes = Quote.query.all()
    if quotes:
        quote = choice(quotes).text
    else:
        quote = "No quotes available."
    return render_template('affirmation.html', quote=quote)

@main_bp.route('/login')
def login():
    redirect_uri = url_for('main.authorized', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@main_bp.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('main.index'))

@main_bp.route('/login/authorized')
def authorized():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('https://www.googleapis.com/oauth2/v1/userinfo')
    user_info = resp.json()
    user = User.query.filter_by(email=user_info['email']).first()
    if user is None:
        user = User(username=user_info['name'], email=user_info['email'])
        db.session.add(user)
        db.session.commit()
    session['user_id'] = user.id
    return redirect(url_for('main.index'))

@main_bp.route('/my_quotes')
def my_quotes():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('main.login'))
    user = User.query.get(user_id)
    return render_template('my_quotes.html', quotes=user.quotes)

@main_bp.route('/delete_quote/<int:quote_id>', methods=['POST'])
def delete_quote(quote_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not logged in'})
    quote = Quote.query.get(quote_id)
    if quote and quote.user_id == user_id:
        db.session.delete(quote)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Quote not found or not authorized'})