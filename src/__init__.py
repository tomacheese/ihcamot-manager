import json
import os

import tweepy


def get_twitter_api():
    path = os.environ.setdefault("CONFIG_PATH", "config.json")
    if not os.path.exists(path):
        print('config not found')
        return
    with open(path, 'r') as f:
        config = json.load(f)
    auth = tweepy.OAuthHandler(
        config["consumer_key"],
        config["consumer_secret"],
        config["access_token"],
        config["access_token_secret"]
    )
    return tweepy.API(auth)
