import base64
import os
import pymongo
from bson import Binary, ObjectId
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

def serialize_recipe(recipe):
    serialized = {
        "id": str(recipe["_id"]),
        **{key: value for key, value in recipe.items() if key not in {"_id", "imageMimeType"}},
    }
    image = recipe.get("image")
    if isinstance(image, bytes):
        content_type = recipe.get("imageMimeType", "image/jpeg")
        serialized["image"] = f"data:{content_type};base64,{base64.b64encode(image).decode('ascii')}"
    return serialized


def prepare_recipe_image(recipe):
    image = recipe.get("image")
    if not isinstance(image, str) or not image.startswith("data:image/"):
        return recipe

    header, _, encoded_image = image.partition(",")
    content_type = header[5:].split(";", 1)[0]
    return {
        **recipe,
        "image": Binary(base64.b64decode(encoded_image, validate=True)),
        "imageMimeType": content_type,
    }
#Public-------------------------------------------------------------------


def get_recipes_public():
    return [serialize_recipe(recipe) for recipe in publiccollection.find()]


def post_recipe_public(recipe, user_id):
    recipe = prepare_recipe_image(recipe)
    recipe = {**recipe, "author": user_id}
    result = publiccollection.insert_one(recipe.copy())
    return serialize_recipe({"_id": result.inserted_id, **recipe})

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

    return serialize_recipe(updated_recipe)

def delete_recipe_public(recipe_id, user_id):
    if not ObjectId.is_valid(recipe_id):
        return None

    result = publiccollection.delete_one({"_id": ObjectId(recipe_id), "author": user_id})
    if result.deleted_count == 0:
        return None

    return {"deleted_count": result.deleted_count}

#Private--------------------------------------------------------------------
def get_recipes_private(user_id):
    privatecollection = db[f"private-{user_id}"]
    return [serialize_recipe(recipe) for recipe in privatecollection.find()]

def post_recipe_private(recipe, user_id):
    privatecollection = db[f"private-{user_id}"]
    recipe = prepare_recipe_image(recipe)
    recipe = {**recipe, "author": user_id}
    result = privatecollection.insert_one(recipe.copy())
    return serialize_recipe({"_id": result.inserted_id, **recipe})

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

    return serialize_recipe(updated_recipe)

def delete_recipe_private(recipe_id, user_id):
    if not ObjectId.is_valid(recipe_id):
        return None

    privatecollection = db[f"private-{user_id}"]
    result = privatecollection.delete_one(
        {"_id": ObjectId(recipe_id), "author": user_id}
    )
    if result.deleted_count == 0:
        return None

    return {"deleted_count": result.deleted_count}

#Favorite---------------------------------------------------------------------

def favorite_recipe(recipe_id, user_id):
    if not ObjectId.is_valid(recipe_id):
        return None

    object_id = ObjectId(recipe_id)

    # Check if the recipe exists in either public or private collection
    public_recipe = publiccollection.find_one(
        {"_id": object_id},
        {"_id": 1},
    )

    privatecollection = db[f"private-{user_id}"]
    private_recipe = privatecollection.find_one(
        {"_id": object_id},
        {"_id": 1},
    )

    if public_recipe is None and private_recipe is None:
        return None

    # Add the recipe to the user's favorites list.
    # $addToSet prevents the same recipe from being added twice.
    db["favorites"].update_one(
        {"_id": user_id},
        {"$addToSet": {"recipe_ids": object_id}},
        upsert=True,
    )

    return {
        "recipeId": str(object_id),
        "userId": user_id,
        "isFavorite": True,
    }


def unfavorite_recipe(recipe_id, user_id):
    if not ObjectId.is_valid(recipe_id):
        return None

    object_id = ObjectId(recipe_id)

    # checks if the recipe exists in public and private collection
    public_recipe = publiccollection.find_one(
        {"_id": object_id},
        {"_id": 1},
    )

    privatecollection = db[f"private-{user_id}"]
    private_recipe = privatecollection.find_one(
        {"_id": object_id},
        {"_id": 1},
    )

    if public_recipe is None and private_recipe is None:
        return None

    # removes recipe from users favorites list
    db["favorites"].update_one(
        {"_id": user_id},
        {"$pull": {"recipe_ids": object_id}},
    )

    # deletes the favorites document if the user has no favorites left
    db["favorites"].delete_one({
        "_id": user_id,
        "recipe_ids": {"$size": 0},
    })

    return {
        "recipeId": str(object_id),
        "userId": user_id,
        "isFavorite": False,
    }


def get_favorite_recipes(user_id):
    favorite_document = db["favorites"].find_one({"_id": user_id})

    if favorite_document is None:
        return []

    recipe_ids = favorite_document.get("recipe_ids", [])

    if not recipe_ids:
        return []

    # Fetch public recipes
    public_recipes = {
        recipe["_id"]: recipe
        for recipe in publiccollection.find({
            "_id": {"$in": recipe_ids}
        })
    }

    # gets user private recipes
    privatecollection = db[f"private-{user_id}"]

    private_recipes = {
        recipe["_id"]: recipe
        for recipe in privatecollection.find({
            "_id": {"$in": recipe_ids}
        })
    }

    # combines public and private recipes
    recipes_by_id = {
        **public_recipes,
        **private_recipes,
    }

    return [
        serialize_recipe({
            **recipes_by_id[recipe_id],
            "isFavorite": True,
        })
        for recipe_id in recipe_ids
        if recipe_id in recipes_by_id
    ]
