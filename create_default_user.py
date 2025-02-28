import os
from app import create_app, db
from app.models import User

app = create_app()

def create_default_user():
    with app.app_context():
        default_user = User.query.filter_by(username='default_user').first()
        if not default_user:
            default_user = User(username='default_user', email='default@example.com')
            db.session.add(default_user)
            db.session.commit()
            print("Default user created.")
        else:
            print("Default user already exists.")

if __name__ == "__main__":
    create_default_user()
    