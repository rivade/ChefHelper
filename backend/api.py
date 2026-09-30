import base64
import binascii
import os
from typing import Annotated
import jwt
from jwt import PyJWKClient, PyJWKClientError
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field, field_validator
import mongo

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

    @field_validator("image")
    @classmethod
    def validate_image_data_url(cls, image: str) -> str:
        if not image.startswith("data:"):
            return image

        header, separator, encoded_image = image.partition(",")
        if not separator or not header.startswith("data:image/") or not header.endswith(";base64"):
            raise ValueError("Image must be a base64-encoded image data URL")

        try:
            base64.b64decode(encoded_image, validate=True)
        except (binascii.Error, ValueError) as error:
            raise ValueError("Image data URL contains invalid base64 data") from error

        return image


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

class FavoriteInfo(BaseModel):
    recipeId: str
    userId: str
    isFavorite: bool

def init():
    load_dotenv()
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    auth0_audience = os.getenv("AUTH0_AUDIENCE")
    if not auth0_domain or not auth0_audience:
        raise RuntimeError("AUTH0_DOMAIN and AUTH0_AUDIENCE must be configured")

    issuer = f"https://{auth0_domain.removeprefix('https://').rstrip('/')}/"
    jwks_client = PyJWKClient(f"{issuer}.well-known/jwks.json")
    bearer_scheme = HTTPBearer(auto_error=False)

    def require_user(
        credentials: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(bearer_scheme),
        ],
    ) -> str:
        if credentials is None:
            raise HTTPException(
                status_code=401,
                detail="Missing bearer token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            token = credentials.credentials
            signing_key = jwks_client.get_signing_key_from_jwt(token).key
            claims = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=auth0_audience,
                issuer=issuer,
                options={"require": ["exp", "sub"]},
            )
            return claims["sub"]
        except (jwt.PyJWTError, PyJWKClientError) as error:
            raise HTTPException(
                status_code=401,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from error

    app = FastAPI(title="ChefHelper API")
    allowed_origins = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://localhost:4173"
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
    def upload_recipe_public(
        recipe: RecipeCreate,
        user_id: str = Depends(require_user),
    ):
        """Upload recipe to public database"""
        return mongo.post_recipe_public(recipe.model_dump(exclude_none=True), user_id)

    @app.patch("/api/recipes/{recipe_id}")
    def patch_recipe_public(
        recipe_id: str,
        recipe: RecipePatch,
        user_id: str = Depends(require_user),
    ):
        """Update recipe in public database"""
        updates = recipe.model_dump(exclude_unset=True)
        if not updates or any(value is None for value in updates.values()):
            raise HTTPException(
                status_code=422,
                detail="Provide at least one non-null recipe field to update",
            )

        updated_recipe = mongo.patch_recipe_public(recipe_id, updates, user_id)
        if updated_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return updated_recipe

    @app.delete("/api/recipes/{recipe_id}")
    def delete_recipe_public(
        recipe_id: str,
        user_id: str = Depends(require_user),
    ):
        """Delete a public recipe by its ID"""
        deleted_recipe = mongo.delete_recipe_public(recipe_id, user_id)
        if deleted_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return deleted_recipe

    #Private--------------------------------------------------------------------------
    @app.get("/api/recipes/private")
    def get_recipes_private(user_id: str = Depends(require_user)):
        """Retrieve private recipes"""
        return mongo.get_recipes_private(user_id)
    
    @app.post("/api/recipes/private", status_code=201)
    def upload_recipe_private(
        recipe: RecipeCreate,
        user_id: str = Depends(require_user),
    ):
        """Upload recipe to users own private collection"""
        return mongo.post_recipe_private(recipe.model_dump(exclude_none=True), user_id)

    @app.patch("/api/recipes/private/{recipe_id}")
    def patch_recipe_private(
        recipe_id: str,
        recipe: RecipePatch,
        user_id: str = Depends(require_user),
    ):
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

    @app.delete("/api/recipes/private/{recipe_id}")
    def delete_recipe_private(
        recipe_id: str,
        user_id: str = Depends(require_user),
    ):
        """Delete a private recipe by its ID"""
        deleted_recipe = mongo.delete_recipe_private(recipe_id, user_id)
        if deleted_recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return deleted_recipe

    #Favorite--------------------------------------------------------------------------
    @app.get("/api/favorites")
    def get_favorite_recipes(user_id: str = Depends(require_user)):
        """Retrieve a user's favorite public recipes"""
        return mongo.get_favorite_recipes(user_id)

    @app.post("/api/favorites/{recipe_id}", response_model=FavoriteInfo)
    def favorite_recipe(
        recipe_id: str,
        user_id: str = Depends(require_user),
    ):
        """Add a public recipe to a user's favorites"""
        favorite = mongo.favorite_recipe(recipe_id, user_id)
        if favorite is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return favorite

    @app.delete("/api/favorites/{recipe_id}", response_model=FavoriteInfo)
    def unfavorite_recipe(
        recipe_id: str,
        user_id: str = Depends(require_user),
    ):
        """Remove a public recipe from a user's favorites"""
        favorite = mongo.unfavorite_recipe(recipe_id, user_id)
        if favorite is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return favorite

    #Images

    return app