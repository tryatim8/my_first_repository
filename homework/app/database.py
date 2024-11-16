from typing import Any

from sqlalchemy import Column, Integer, String, desc
from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///homework/app/hw.db"

Base: Any = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionmaker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
async_session = AsyncSessionmaker()


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    views = Column(Integer, default=0, index=True)
    name = Column(String, nullable=False)
    minutes_to_cook = Column(Integer, nullable=False, index=True)

    ingredients = Column(String, nullable=False, index=True)
    description = Column(String, index=True)

    @classmethod
    async def recipe(cls, recipe_id):
        """Возвращает запись рецепта и прибавляет к нему 1 просмотр"""
        res = (
            await async_session.execute(
                select(Recipe).filter(Recipe.id == recipe_id)
            )
        ).scalar()
        res.views += 1
        await async_session.commit()
        return res

    @classmethod
    async def recipes(cls):
        """Возвращает список записей рецептов с сортировкой по просмотрам"""
        res = (
            (await async_session.execute(
                select(Recipe).order_by(desc(Recipe.views))
            ))
            .scalars()
            .all()
        )
        for elem in res:
            elem.views += 1
        await async_session.commit()
        return res
