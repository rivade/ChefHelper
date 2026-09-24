import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import mongo


class RecipeCreate(BaseModel):
    author: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    ingredients: str = Field(min_length=1)
    instructions: str = Field(min_length=1)
    cookingtime: list[int] = Field(min_length=2, max_length=2)
    portions: int = Field(gt=0, le=100)
    difficulty: int = Field(ge=1, le=5)

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


def init():
    app = FastAPI(title="StudyBoard API")
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
    
    @app.get("/")
    def home():
        """Health check endpoint"""
        return {"message": "API fungerar"}
    
    @app.get("/api/recipes")
    def get_recipes():
        """Retrieve all recipes"""
        return mongo.get_recipes()
    
    @app.post("/api/recipes", status_code=201)
    def upload_recipe_public(recipe: RecipeCreate):
        """Upload recipe to public database"""
        return mongo.post_recipe_public(recipe.model_dump())

    @app.post("/api/recipes/private/{user_id}", status_code=201)
    def upload_recipe_private(recipe: RecipeCreate, user_id: str):
        """Upload recipe to users own private collection"""
        return mongo.post_recipe_private(recipe.model_dump(), user_id)

    @app.delete("/api/recipes/{recipe_id}")
    def delete_recipe_public(recipe_id: str):
        """Delete a public recipe by its ID"""
        return mongo.delete_recipe_public(recipe_id)
    
    @app.delete("/api/recipes/private/{user_id}/{recipe_id}")
    def delete_recipe_private(recipe_id: str, user_id: str):
        """Delete a private recipe by its ID"""
        return mongo.delete_recipe_private(recipe_id, user_id)

    return app