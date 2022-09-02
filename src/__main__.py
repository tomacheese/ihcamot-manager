import re
import threading
import time
from pprint import pprint

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from src import get_account, get_accounts

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/favorite/{tweet_id}")
async def favorite(tweet_id: str):
    print("Add favorite to tweet:", tweet_id)
    try:
        account = get_account('ihc_amot')
        api = account['api']
        api.create_favorite(tweet_id)
        return {"status": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def run():
    print("run()")
    while True:
        try:
            accounts = get_accounts()
            for account in accounts:
                check_direct_message(get_account(account))
            print("End")
        except Exception as e:
            print("error")
            print(e)
        # 1 minute
        time.sleep(60)


def check_direct_message(account):
    print("check_direct_message()")
    regex = r"https://twitter.com/[^/]+/status/([0-9]+)"

    api = account['api']
    sender_id = account['sender_id']

    messages = api.get_direct_messages()
    for obj in messages:
        message = obj.message_create
        if message["sender_id"] != sender_id:
            continue
        message_data = message["message_data"]

        text = message_data["text"]
        urls = message_data["entities"]["urls"]

        for url in urls:
            text = str(text).replace(url["url"], url["expanded_url"])

        tweet_id = re.search(regex, text).group(1)
        tweet = api.get_status(tweet_id)
        if tweet.favorited:
            print("Already favorite: ", tweet_id)
            api.mark_direct_message_read(obj.id, message["target"]["recipient_id"])
            continue
        api.create_favorite(tweet.id)
        api.mark_direct_message_read(obj.id, message["target"]["recipient_id"])

        print("Add favorite to tweet:", tweet_id)


if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

    uvicorn.run(app, host="0.0.0.0", port=80)
