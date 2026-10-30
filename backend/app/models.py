from sqlalchemy import JSON, Boolean, Column, Integer, String, Text

from .database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    cuisine = Column(String(60), nullable=True)
    category = Column(String(20), nullable=False)
    cook_time_minutes = Column(Integer, nullable=False)
    servings = Column(Integer, nullable=False, default=4)
    ingredients = Column(JSON, nullable=False, default=list)
    instructions = Column(Text, nullable=True)
    favorite = Column(Boolean, nullable=False, default=False)
