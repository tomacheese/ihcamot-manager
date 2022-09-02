import json
import os

import tweepy


def get_twitter_api(consumer_key: str,
                    consumer_secret: str,
                    access_token: str,
                    access_token_secret: str):
    auth = tweepy.OAuthHandler(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )
    return tweepy.API(auth)


def get_account(account: str):
    path = os.environ.setdefault("CONFIG_PATH", "config.json")
    if not os.path.exists(path):
        print('config not found')
        return
    with open(path, 'r') as f:
        config = json.load(f)
    if account not in config:
        print('account config not found')
        return
    account = config[account]
    return {
        'api': get_twitter_api(
            account['consumer_key'],
            account['consumer_secret'],
            account['access_token'],
            account['access_token_secret']
        ),
        'sender_id': account['sender_id']
    }


def get_accounts():
    path = os.environ.setdefault("CONFIG_PATH", "config.json")
    if not os.path.exists(path):
        print('config not found')
        return
    with open(path, 'r') as f:
        config = json.load(f)
    return list(config.keys())
