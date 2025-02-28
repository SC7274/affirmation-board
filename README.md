# Affirmation Board

Affirmation Board is a web application that allows users exchange uplifting quotes. 

Users can log in using their Google account, submit their own quotes, view quotes submitted by others, and delete their own quotes.

## Features

- User authentication via Google OAuth
- Submit uplifting quotes
- View random quotes on the main page
- View and delete quotes you submitted

  ![image](https://github.com/user-attachments/assets/87f2aefd-30f2-4283-883b-c566feb5d08e)


## Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- Authlib (for Google OAuth)
- HTML/CSS
- JavaScript

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- PostgreSQL (or any other supported database)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SC7274/affirmation-board.git
   cd affirmation-board
   ```
2. Create a virtual environment and activate it:
    ``` python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
4. Set up the database:
    ```
    flask db upgrade
    ```

5. Create a default user and populate the database with default quotes:
    ```
    python create_default_user.py
    python populate_quotes.py
    ```


6. Create a `config.py` file in the root directory with the following content:

    ```python
    import os

    class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        OAUTH_CREDENTIALS = {
            'google': {
                'id': 'your_google_client_id',
                'secret': 'your_google_client_secret'
            }
        }
    ```

    Replace `your_secret_key`, `your_google_client_id`, and `your_google_client_secret` with your actual credentials.

### Running the Application

1. Set the Flask application environment variable:

    ```bash
    export FLASK_APP=app:create_app  # On Windows, use `set FLASK_APP=app:create_app`
    ```

2. Run the Flask application:

    ```bash
    flask run
    ```

3. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

- **Submit a Quote**: Enter your uplifting message in the input field and click "Submit".
- **View Quotes**: The main page displays a random quote from the database.
- **My Quotes**: View and delete your own submitted quotes by navigating to the "My Quotes" page.



## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Authlib](https://authlib.org/)
- [Unsplash](https://unsplash.com/) for the background image
