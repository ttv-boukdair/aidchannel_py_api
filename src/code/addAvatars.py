import os
import twint
import concurrent.futures
from itertools import repeat
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId



DB = "mongodb://aidchannel:aidchannel_password123456@51.77.134.195:27028/aidchannel?authSource=aidchannel"
cloud_client=MongoClient(DB)
db = cloud_client.aidchannel


def get_org_infos():
    has_accounts = {}
    cursor_account = db.organizations.find({"twitter_username": {"$exists": True}})
    for c1 in cursor_account:
        info = {
        "org_id":  c1["_id"]
        }
        has_accounts[c1["twitter_username"]] = info
    twt_usernames = list(has_accounts.keys())
    organization_ids = [has_accounts[user]["org_id"] for user in twt_usernames]
    return twt_usernames, organization_ids


def save_avatar(username,organization_id):
    exists =  db.twitters_avatars.find({"organization": ObjectId(organization_id)}).distinct("organization")

    if len(exists) != 0 :
        return None

    c = twint.Config()
    c.Username = username
    c.Store_object = True

    try:
        twint.run.Lookup(c)

    except Exception as e:
        print("could not get avatar of ", username, e)
        return None
    user = twint.output.users_list[0]

    model={"avatar" : user.avatar ,
           "organization":organization_id,
           "username":username}

    document = db.twitters_avatars.insert_one(model)

def run():
    twt_usernames, organization_ids = get_org_infos()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda params: save_avatar(*params), zip(twt_usernames, organization_ids))




