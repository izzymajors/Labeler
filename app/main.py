from flask import Flask, render_template, request
import pandas as pd

from Fortuna import RandomValue

from app.db_ops import insert_data, load_data

APP = Flask(__name__)
random_tweet = RandomValue(pd.read_csv('app/data/data.csv')['tweets'])


@APP.route("/", methods=['GET', 'POST'])
def home():
    rank = request.form.get("rank")
    tweet = request.form.get("tweet")
    if rank and tweet:
        insert_data(tweet, int(rank))
    return render_template(
        "home.html",
        tweet=random_tweet(),
    )


@APP.route("/ranks/")
def ranks():
    return render_template(
        "ranks.html",
        tweets=load_data(),
    )


if __name__ == '__main__':
    APP.run()
