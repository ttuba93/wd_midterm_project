from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe Book API", version="1.0.0")


def get_or_404(db: Session, recipe_id: int):
    recipe = db.get(models.Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/recipes", response_model=List[schemas.RecipeOut])
def list_recipes(
    category: Optional[schemas.Category] = None,
    cuisine: Optional[str] = None,
    favorite: Optional[bool] = None,
    max_time: Optional[int] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Recipe)
    if category is not None:
        query = query.filter(models.Recipe.category == category.value)
    if cuisine is not None:
        query = query.filter(models.Recipe.cuisine.ilike(cuisine))
    if favorite is not None:
        query = query.filter(models.Recipe.favorite == favorite)
    if max_time is not None:
        query = query.filter(models.Recipe.cook_time_minutes <= max_time)
    if q:
        query = query.filter(models.Recipe.title.ilike(f"%{q}%"))
    return query.order_by(models.Recipe.id).all()


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return get_or_404(db, recipe_id)


@app.post("/recipes", response_model=schemas.RecipeOut, status_code=status.HTTP_201_CREATED)
def create_recipe(data: schemas.RecipeIn, db: Session = Depends(get_db)):
    recipe = models.Recipe(**data.model_dump(mode="json"))
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@app.put("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
def update_recipe(recipe_id: int, data: schemas.RecipeIn, db: Session = Depends(get_db)):
    recipe = get_or_404(db, recipe_id)
    for key, value in data.model_dump(mode="json").items():
        setattr(recipe, key, value)
    db.commit()
    db.refresh(recipe)
    return recipe


@app.patch("/recipes/{recipe_id}/favorite", response_model=schemas.RecipeOut)
def set_favorite(recipe_id: int, data: schemas.FavoriteUpdate, db: Session = Depends(get_db)):
    recipe = get_or_404(db, recipe_id)
    recipe.favorite = data.favorite
    db.commit()
    db.refresh(recipe)
    return recipe


@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = get_or_404(db, recipe_id)
    db.delete(recipe)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
