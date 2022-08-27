import re
import threading
import time

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from src import get_twitter_api

api = get_twitter_api()

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
        api.create_favorite(tweet_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



def check_direct_message():
    regex = r"https://twitter.com/[^/]+/status/([0-9]+)"
    while True:
        try:
            print("Check direct messages")
            messages = api.get_direct_messages()
            for obj in messages:
                message = obj.message_create
                if message["sender_id"] != '286048624':
                    continue  # only book000
                message_data = message["message_data"]

                text = message_data["text"]
                urls = message_data["entities"]["urls"]

                for url in urls:
                    text = str(text).replace(url["url"], url["expanded_url"])

                tweet_id = re.search(regex, text).group(1)
                tweet = api.get_status(tweet_id)
                if tweet.favorited:
                    print("Already favorited: ", tweet_id)
                    continue
                api.create_favorite(tweet.id)

                print("Add favorite to tweet:", tweet_id)
            print("End")
        except Exception as e:
            print("error")
            print(e)
        # 1 minute
        time.sleep(60)


if __name__ == '__main__':
    t = threading.Thread(target=check_direct_message)
    t.daemon = True
    t.start()

    uvicorn.run(app, host="0.0.0.0", port=80)
