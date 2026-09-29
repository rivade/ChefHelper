import os
import json
import pymongo
from bson import ObjectId
from bson import json_util
from dotenv import load_dotenv
from pymongo import ReturnDocument
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

    global publiccollection
    publiccollection = db['publicrecipes']


def test_connection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    print(client.list_database_names())

#Public-------------------------------------------------------------------
def get_recipes_public():
    return json.loads(json_util.dumps(publiccollection.find()))


def post_recipe_public(recipe):
    result = publiccollection.insert_one(recipe.copy())
    return {
        "_id": str(result.inserted_id),
        **recipe
    }

def patch_recipe_public(recipe_id, updates):
    if not ObjectId.is_valid(recipe_id):
        return None

    updated_recipe = publiccollection.find_one_and_update(
        {"_id": ObjectId(recipe_id)},
        {"$set": updates},
        return_document=ReturnDocument.AFTER,
    )
    if updated_recipe is None:
        return None

    updated_recipe["_id"] = str(updated_recipe["_id"])
    return updated_recipe

def delete_recipe_public(recipe_id):
    result = publiccollection.delete_one({"_id": ObjectId(recipe_id)})
    return {"deleted_count": result.deleted_count}

#Private--------------------------------------------------------------------
def get_recipes_private(user_id):
    privatecollection = db[f"private-{user_id}"]
    return json.loads(json_util.dumps(privatecollection.find()))

def post_recipe_private(recipe, user_id):
    privatecollection = db[f"private-{user_id}"]
    result = privatecollection.insert_one(recipe.copy())
    return {
        "_id": str(result.inserted_id),
        **recipe
    }

def patch_recipe_private(recipe_id, updates, user_id):
    if not ObjectId.is_valid(recipe_id):
        return None

    privatecollection = db[f"private-{user_id}"]
    updated_recipe = privatecollection.find_one_and_update(
        {"_id": ObjectId(recipe_id)},
        {"$set": updates},
        return_document=ReturnDocument.AFTER,
    )
    if updated_recipe is None:
        return None

    updated_recipe["_id"] = str(updated_recipe["_id"])
    return updated_recipe

def delete_recipe_private(recipe_id, user_id):
    privatecollection = db[f"private-{user_id}"]
    result = privatecollection.delete_one({"_id": ObjectId(recipe_id)})
    return {"deleted_count": result.deleted_count}