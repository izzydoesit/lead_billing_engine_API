# This is where we define our base model
from sqlalchemy.ext.declarative import declarative_base  # Base class for models

DeclarativeBase = declarative_base()


class ModelBase(DeclarativeBase):
    pass
