
# importing Flask and other modules
from flask import Flask, request, render_template, redirect, url_for
from random import randint


app = Flask(__name__)


@app.route("/")
def index():
    quotes_txt = open("quotes.txt", "r")
    quotes_list = quotes_txt.read().split("\n")
    randomNumber = randint(0,len(quotes_list)-1)
    quote = quotes_list[randomNumber]
    quotes_txt.close()
    return render_template('affirmation.html', quote = quote)


@app.route('/', methods=['POST'])
def my_form_post():
    quotes_txt = open("quotes.txt", "a")
    message = request.form['user_quote']
    processed_text = message.upper()
    quotes_txt.write("\n" + processed_text)
    quotes_txt.close()

    quotes_txt = open("quotes.txt", "r")
    quotes_list = quotes_txt.read().split("\n")
    randomNumber = randint(0,len(quotes_list)-1)
    quote = quotes_list[randomNumber]
    quotes_txt.close()
    return render_template('affirmation.html', quote = quote)


 



if __name__ == "__main__":
    app.run(debug = True, port=5000)
