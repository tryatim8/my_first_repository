from typing import Optional

from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    """Базовая модель рецепта"""

    name: str
    minutes_to_cook: int = Field(..., ge=1)


class RecipeIn(BaseRecipe):
    """Модель создания рецепта"""

    ingredients: str
    description: Optional[str] = None


class RecipeOut(RecipeIn):
    """Модель для возвращения рецепта"""

    id: int

    class Config:
        from_attributes = True


class RecipeMultipleOut(BaseRecipe):
    """Модель для списка рецептов"""

    id: int
    views: int = 0

    class Config:
        from_attributes = True
