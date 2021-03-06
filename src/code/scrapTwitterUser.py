import os
import twint
import concurrent.futures
from itertools import repeat
from pymongo import MongoClient
from datetime import datetime, timedelta

DB = "mongodb://aidchannel:aidchannel_password123456@51.77.134.195:27028/aidchannel?authSource=aidchannel"

client=MongoClient(DB)
db = client.aidchannel

def get_last_date(username):
    try:
        cur = db.twitters.find({"twitter_username":username}).sort("posted_at",-1).limit(1)
        for doc in cur :
            date = doc['posted_at']
            date2 = date[:18]+str(int(date[18]) + 1 )
            return date2
            # "2021-07-17 21:50:03"
    except Exception as e:
        print("could not get last date of: ",username,"\n",e)
        return False

def get_org_info():

    has_accounts = {}
    cursor_account = db.organizations.find({"twitter_username": {"$exists": True}, "country":{"$exists": True}})
    for c1 in cursor_account:
        info = {
        "org_id":  c1["_id"],
        "country": c1["country"],
        }
        has_accounts[c1["twitter_username"]] = info

    twt_usernames = list(has_accounts.keys())
    organization_ids = [has_accounts[user]["org_id"] for user in twt_usernames]
    country_ids = [has_accounts[user]["country"] for user in twt_usernames]

    return twt_usernames, organization_ids, country_ids


def containsTweet(id):
   cur = db.twitters.find({'tweet_id':id,'$where': "this.twitter_username.toLowerCase() === this.tweet_username.toLowerCase()" }).limit(1)
   for tweet in cur:
      if tweet:
        return True
   return False

def save_model(tweet, username, org_id, country_id):
    datestamp = tweet.datestamp
    timestamp = tweet.timestamp
    posted_at = datestamp + " " +  timestamp
    try:
        avatar = db.twitters_avatars.find({"username":username}).limit(1).distinct("avatar")[0]
    except:
        avatar = ""
        print("could not find avatar of", username," from db")
    
    model = {
    "tweet_id": tweet.id,
    "twitter_username": username,
    "tweet_username":tweet.username,
    "organization": org_id,
    "country": country_id,
    "posted_at": posted_at,
    "body":tweet.tweet,
    "photos":tweet.photos,
    "name":tweet.name,
    "avatar_id": avatar,
     "validation":0
    }
    if(containsTweet(tweet.id)):
        pass
    else:
        document = db.twitters.insert_one(model)


def scrap_users_tweets(username, organization_id, country_id):
    db = client["aidchannel"]
    c = twint.Config()
    c.Username = username
    c.Custom["tweet"] = ["id","created_at","datestamp"]
    c.Filter_retweets = True
    # c.Retweets = True
    c.Limit = 10
    c.Retries_count = 5
    c.Store_object = True
    # c.Hide_output = True

    #  add newest tweets to database since last scrapping
    since_date = get_last_date(username)
    # yesterday date
    yesterday = datetime.now() - timedelta(1)
    d = datetime.strftime(yesterday, '%Y-%m-%d')
    c.Since = d
    try:
        twint.run.Search(c)
    except Exception as e:
        print("could not fetch data from: ", username,"\n",e)
        return None

    tweets = twint.output.tweets_list
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda params: save_model(*params), zip(tweets, repeat(username), repeat(organization_id), repeat(country_id)))


def run():
    usernames, org_ids, country_ids = get_org_info()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda params: scrap_users_tweets(*params), zip(usernames,org_ids,country_ids))
        print("great")
    clean()

def clean():
    db.twitters.remove({'$where': "this.twitter_username.toLowerCase() !== this.tweet_username.toLowerCase()"})