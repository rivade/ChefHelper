import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator
import mongo

#TODO Add security to API


class RecipeCreate(BaseModel):
    id: str | None = Field(default=None, exclude=True)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    image: str
    imagePosition: str | None = None
    difficulty: int | str
    time: str = Field(min_length=1)
    servings: str = Field(min_length=1)
    ingredients: str = Field(min_length=1)
    instructions: str | None = Field(default=None, min_length=1)
    isUserCreated: bool | None = None


class RecipePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str | None = Field(default=None, exclude=True)
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    image: str | None = None
    imagePosition: str | None = None
    difficulty: int | str | None = None
    time: str | None = Field(default=None, min_length=1)
    servings: str | None = Field(default=None, min_length=1)
    ingredients: str | None = Field(default=None, min_length=1)
    instructions: str | None = Field(default=None, min_length=1)
    isUserCreated: bool | None = None


def init():
    app = FastAPI(title="ChefHelper API")
    allowed_origins = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:4173"
        ).split(",")
        if origin.strip()
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #Public--------------------------------------------------------------------------
    @app.get("/")
    def home():
        """Health check endpoint"""
        return {"message": "API fungerar"}
    
    @app.get("/api/recipes")
    def get_recipes_public():
        """Retrieve public recipes"""
        return mongo.get_recipes_public()
    
    @app.post("/api/recipes/{user_id}", status_code=201)
    def upload_recipe_public(user_id: str, recipe: RecipeCreate):
        """Upload recipe to public database"""
        return mongo.post_recipe_public(recipe.model_dump(exclude_none=True), user_id)

    @app.patch("/api/recipes/{user_id}/{recipe_id}")
    def patch_recipe_public(user_id: str, recipe_id: str, recipe: RecipePatch):
        """Update recipe in public database"""
        updates = recipe.model_dump(exclude_unset=True)
        if not updates or any(value is None for value in updates.values()):
            raise HTTPException(
                status_code=422,
                detail="Provide at least one non-null recipe field to update",
            )

        updated_recipe = mongo.patch_recipe_public(recipe_id, updates, user_id)
        if updated_recipe is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return updated_recipe

    @app.delete("/api/recipes/{recipe_id}")
    def delete_recipe_public(recipe_id: str):
        """Delete a public recipe by its ID"""
        return mongo.delete_recipe_public(recipe_id)

    #Private--------------------------------------------------------------------------
    @app.get("/api/recipes/private/{user_id}")
    def get_recipes_private(user_id: str):
        """Retrieve private recipes"""
        return mongo.get_recipes_private(user_id)
    
    @app.post("/api/recipes/private/{user_id}", status_code=201)
    def upload_recipe_private(recipe: RecipeCreate, user_id: str):
        """Upload recipe to users own private collection"""
        return mongo.post_recipe_private(recipe.model_dump(exclude_none=True), user_id)

    @app.patch("/api/recipes/private/{user_id}/{recipe_id}")
    def patch_recipe_private(user_id: str, recipe_id: str, recipe: RecipePatch):
        """Update a recipe in the user's private collection"""
        updates = recipe.model_dump(exclude_unset=True)
        if not updates or any(value is None for value in updates.values()):
            raise HTTPException(
                status_code=422,
                detail="Provide at least one non-null recipe field to update",
            )

        updated_recipe = mongo.patch_recipe_private(recipe_id, updates, user_id)
        if updated_recipe is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return updated_recipe

    @app.delete("/api/recipes/private/{user_id}/{recipe_id}")
    def delete_recipe_private(recipe_id: str, user_id: str):
        """Delete a private recipe by its ID"""
        return mongo.delete_recipe_private(recipe_id, user_id)

    return app