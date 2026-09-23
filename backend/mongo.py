import os
import json
import pymongo
from bson import ObjectId
from bson import json_util
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

def init():
    load_dotenv()

    uri = os.getenv('MONGODB_URI')

    global db_name
    db_name = "chefhelper"

    global client
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

    global db
    db = client[db_name]

    global collection
    collection = db['publicrecipes']


def test_connection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    print(client.list_database_names())

def get_recipes():
    return json.loads(json_util.dumps(collection.find()))

def post_recipe(recipe):
    result = collection.insert_one(recipe.copy())
    return {
        "_id": str(result.inserted_id),
        **recipe
    }

def delete_recipe(recipe_id):
    result = collection.delete_one({"_id": ObjectId(recipe_id)})
    return {"deleted_count": result.deleted_count}