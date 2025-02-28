import os
from app import create_app, db
from app.models import Quote, User

app = create_app()

def populate_quotes():
    with app.app_context():
        default_user = User.query.filter_by(username='default_user').first()
        if not default_user:
            print("Default user not found. Please create a default user first.")
            return

        with open('default_quotes.txt', 'r') as file:
            quotes = file.readlines()
            for quote in quotes:
                quote = quote.strip()
                if quote:
                    new_quote = Quote(text=quote, user_id=default_user.id)  # Assign to default user
                    db.session.add(new_quote)
            db.session.commit()
            print("Default quotes added to the database.")

if __name__ == "__main__":
    populate_quotes()
    