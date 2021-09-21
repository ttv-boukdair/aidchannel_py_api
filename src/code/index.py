import requesttest
import scrapTwitterUser
import scrapNews
import addAvatars
import testselenium
import scrapNews2
import test2
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from pymongo import MongoClient
from typing import Optional



DATA_PATH = '/www/data/'
app = FastAPI(debug = True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class Input(BaseModel):
    text: str


@app.post('/tweets')
def save_tweets():
    tweets = scrapTwitterUser.run()
    print("ok")
    # return tweets


@app.post('/addavatars')
def save_avatar():
    avatars = addAvatars.run()
    print(avatars)
    return avatars


@app.post("/addNews")
def save_news():
    news=scrapNews.addOrgArticles()
    print(news)
    return news


@app.post("/testnews")
def test():
    data = scrapNews2.run()
    # return data

@app.get("/teest")
def teest():
    data = requesttest.run()
    return data






if __name__ == '__main__':
      uvicorn.run(app, host='0.0.0.0',port = 80)
