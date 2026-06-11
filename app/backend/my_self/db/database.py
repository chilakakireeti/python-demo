from dotenv import load_dotenv
import os
from pymongo import MongoClient
from db.db_helper import add_user_helper,fetch_user_helper
import certifi
load_dotenv()
try:
    MONGO_URL = os.getenv("MONGO_URL")
    client=MongoClient(MONGO_URL,tlsCAFile=certifi.where())
    db=client['users_db']
    signup_collection=db['signup_users']
    login_collection=db['login_users']
except Exception as e:
    print(str(e))  

async def add_user(data):
    signup_collection.insert_one(add_user_helper(data))   
    return  True
async def fetch_user(data):
    result= signup_collection.find_one(fetch_user_helper(data))
    return result
async def update_user(filter_query, update_data):
    return  signup_collection.update_one(
        filter_query,
        {"$set": update_data}
    )