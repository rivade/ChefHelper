import os
import pymongo
from bson import ObjectId
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
def _serialize_recipe(recipe):
    return {
        "id": str(recipe["_id"]),
        **{key: value for key, value in recipe.items() if key != "_id"},
    }


def get_recipes_public():
    return [_serialize_recipe(recipe) for recipe in publiccollection.find()]


def post_recipe_public(recipe, user_id):
    recipe = {**recipe, "author": user_id}
    result = publiccollection.insert_one(recipe.copy())
    return _serialize_recipe({"_id": result.inserted_id, **recipe})

def patch_recipe_public(recipe_id, updates, user_id):
    if not ObjectId.is_valid(recipe_id):
        return None

    updated_recipe = publiccollection.find_one_and_update(
        {"_id": ObjectId(recipe_id), "author": user_id},
        {"$set": updates},
        return_document=ReturnDocument.AFTER,
    )
    if updated_recipe is None:
        return None

    return _serialize_recipe(updated_recipe)

def delete_recipe_public(recipe_id):
    result = publiccollection.delete_one({"_id": ObjectId(recipe_id)})
    return {"deleted_count": result.deleted_count}

#Private--------------------------------------------------------------------
def get_recipes_private(user_id):
    privatecollection = db[f"private-{user_id}"]
    return [_serialize_recipe(recipe) for recipe in privatecollection.find()]

def post_recipe_private(recipe, user_id):
    privatecollection = db[f"private-{user_id}"]
    recipe = {**recipe, "author": user_id}
    result = privatecollection.insert_one(recipe.copy())
    return _serialize_recipe({"_id": result.inserted_id, **recipe})

def patch_recipe_private(recipe_id, updates, user_id):
    if not ObjectId.is_valid(recipe_id):
        return None

    privatecollection = db[f"private-{user_id}"]
    updated_recipe = privatecollection.find_one_and_update(
        {"_id": ObjectId(recipe_id), "author": user_id},
        {"$set": updates},
        return_document=ReturnDocument.AFTER,
    )
    if updated_recipe is None:
        return None

    return _serialize_recipe(updated_recipe)

def delete_recipe_private(recipe_id, user_id):
    privatecollection = db[f"private-{user_id}"]
    result = privatecollection.delete_one({"_id": ObjectId(recipe_id)})
    return {"deleted_count": result.deleted_count}