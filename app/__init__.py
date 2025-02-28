from flask import Flask
from app.models import db
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)

    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['OAUTH_CREDENTIALS']['google']['id'],
        client_secret=app.config['OAUTH_CREDENTIALS']['google']['secret'],
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        refresh_token_url=None,
        redirect_uri='http://127.0.0.1:5000/login/authorized',
        client_kwargs={'scope': 'email profile'},
    )

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
