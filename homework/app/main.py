from typing import List
from contextlib import  asynccontextmanager

import uvicorn
from fastapi import FastAPI

from homework.app.database import engine, async_session, Base, Recipe
from homework.app.schemas import RecipeIn, RecipeOut, RecipeMultipleOut


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Выполнение со startup до shutdown кода приложения FastAPI"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async_session.close()
    engine.dispose()

def create_app(_lifespan=None):
    return FastAPI(lifespan=lifespan)


def connect_routes(app: FastAPI):
    @app.get('/')
    async def root():
        return {'message': 'hello world'}


    @app.get('/recipes', response_model=List[RecipeMultipleOut])
    async def recipes() -> List[Recipe]:
        """Возвращает список рецептов с сортировкой по просмотрам"""
        return await Recipe.recipes()


    @app.get('/recipes/{recipe_id}', response_model=RecipeOut)
    async def recipes(recipe_id: int) -> Recipe:
        """Возвращает информацию о рецепте и прибавляет к нему 1 просмотр"""
        return await Recipe.recipe(recipe_id)


    @app.post('/recipes', response_model=RecipeOut)
    async def recipes(recipe: RecipeIn) -> Recipe:
        """Создаёт новый рецепт и возвращает его с присвоенным id"""
        new_recipe = Recipe(**recipe.model_dump())
        async with async_session.begin():
            async_session.add(new_recipe)
        return new_recipe


if __name__ == '__main__':
    app = create_app(_lifespan=lifespan)
    connect_routes(app=app)
    uvicorn.run(app, host='127.0.0.1', port=5000)
