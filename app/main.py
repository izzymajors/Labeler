import random

from flask import Flask, render_template, request
import pandas as pd

from app.db_ops import insert_data, load_data

APP = Flask(__name__)
all_tweets = pd.read_csv('app/data/data.csv')['tweets']


def random_tweet():
    return random.choice(all_tweets)


@APP.route("/", methods=['GET', 'POST'])
def home():
    rank = request.form.get("rank")
    tweet = request.form.get("tweet")
    if rank in {'0', '1', '2', '3', '4', '5'} and tweet:
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
