from pydantic import BaseModel, Field, field_validator

class RecipeCreate(BaseModel):
    author: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    ingredients: str = Field(min_length=1)
    instructions: str = Field(min_length=1)
    cookingtime: list[int] = Field(min_length=2, max_length=2)
    portions: int = Field(gt=0)
    difficulty: int = Field(ge=1, le=5)

    @field_validator("cookingtime")
    @classmethod
    def validate_cookingtime(cls, value: list[int]) -> list[int]:
        if len(value) != 2:
            raise ValueError("cookingtime måste innehålla exakt [timmar, minuter]")
        if value[0] < 0 or value[0] > 72:
            raise ValueError("cookingtime timmar måste vara mellan 0 och 72")
        if value[1] < 0 or value[1] > 59:
            raise ValueError("cookingtime minuter måste vara mellan 0 och 59")
        return value