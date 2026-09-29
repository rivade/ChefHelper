import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator
import mongo


class RecipeCreate(BaseModel):
    author: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    ingredients: str = Field(min_length=1)
    instructions: str = Field(min_length=1)
    cookingtime: list[int] = Field(min_length=2, max_length=2)
    portions: int = Field(gt=0, le=100)
    difficulty: int = Field(ge=1, le=3)

    @field_validator("cookingtime")
    @classmethod
    def validate_cookingtime(cls, value: list[int]) -> list[int]:
        if value[0] > 72:
            raise ValueError("cookingtime hours cannot exceed 72")
        if value[1] > 59:
            raise ValueError("cookingtime minutes cannot exceed 59")
        if value[0] < 0 or value[1] < 0:
            raise ValueError("cookingtime values cannot be negative")
        return value


class RecipePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author: str | None = Field(default=None, min_length=1)
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    ingredients: str | None = Field(default=None, min_length=1)
    instructions: str | None = Field(default=None, min_length=1)
    cookingtime: list[int] | None = Field(default=None, min_length=2, max_length=2)
    portions: int | None = Field(default=None, gt=0, le=100)
    difficulty: int | None = Field(default=None, ge=1, le=3)

    @field_validator("cookingtime")
    @classmethod
    def validate_cookingtime(cls, value: list[int] | None) -> list[int] | None:
        if value is None:
            return value
        if value[0] > 72:
            raise ValueError("cookingtime hours cannot exceed 72")
        if value[1] > 59:
            raise ValueError("cookingtime minutes cannot exceed 59")
        if value[0] < 0 or value[1] < 0:
            raise ValueError("cookingtime values cannot be negative")
        return value


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
    
    @app.post("/api/recipes", status_code=201)
    def upload_recipe_public(recipe: RecipeCreate):
        """Upload recipe to public database"""
        return mongo.post_recipe_public(recipe.model_dump())

    @app.patch("/api/recipes/{recipe_id}")
    def patch_recipe_public(recipe_id: str, recipe: RecipePatch):
        """Update recipe in public database"""
        updates = recipe.model_dump(exclude_unset=True)
        if not updates or any(value is None for value in updates.values()):
            raise HTTPException(
                status_code=422,
                detail="Provide at least one non-null recipe field to update",
            )

        updated_recipe = mongo.patch_recipe_public(recipe_id, updates)
        if updated_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
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
        return mongo.post_recipe_private(recipe.model_dump(), user_id)

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
            raise HTTPException(status_code=404, detail="Recipe not found")
        return updated_recipe

    @app.delete("/api/recipes/private/{user_id}/{recipe_id}")
    def delete_recipe_private(recipe_id: str, user_id: str):
        """Delete a private recipe by its ID"""
        return mongo.delete_recipe_private(recipe_id, user_id)

    return app