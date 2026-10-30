from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Category(str, Enum):
    soup = "soup"
    main = "main"
    salad = "salad"
    dessert = "dessert"
    baking = "baking"
    drink = "drink"


class Ingredient(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    amount: Optional[str] = Field(None, max_length=50, examples=["500 g"])


class RecipeIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    cuisine: Optional[str] = Field(None, max_length=60)
    category: Category
    cook_time_minutes: int = Field(..., ge=1, le=1440)
    servings: int = Field(4, ge=1, le=100)
    ingredients: List[Ingredient] = []
    instructions: Optional[str] = None
    favorite: bool = False


class RecipeOut(RecipeIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class FavoriteUpdate(BaseModel):
    favorite: bool
