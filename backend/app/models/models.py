# This is where we define our base model

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# from sqlalchemy.ext.declarative import declarative_base


class ModelBase(AsyncAttrs, DeclarativeBase):
    pass
