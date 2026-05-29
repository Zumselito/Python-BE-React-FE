from fastapi import APIRouter, HTTPException, Query, status

from app.models.ingredient import (
    Ingredient,
    IngredientCreate,
    IngredientListResponse,
    IngredientUpdate,
)
from app.services.ingredient_service import ingredient_service

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/", response_model=IngredientListResponse)
def list_ingredients(
    category: str | None = Query(default=None, description="Kategorie-Filter"),
    search: str | None = Query(default=None, description="Suche in Name"),
    last_key: str | None = Query(default=None, description="Pagination-Cursor"),
    limit: int = Query(default=50, ge=1, le=200),
):
    return ingredient_service.list(category=category, search=search, last_key=last_key, limit=limit)


@router.post("/", response_model=Ingredient, status_code=status.HTTP_201_CREATED)
def create_ingredient(data: IngredientCreate):
    return ingredient_service.create(data)


@router.get("/{ingredient_id}", response_model=Ingredient)
def get_ingredient(ingredient_id: str):
    ingredient = ingredient_service.get(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Zutat nicht gefunden")
    return ingredient


@router.patch("/{ingredient_id}", response_model=Ingredient)
def update_ingredient(ingredient_id: str, data: IngredientUpdate):
    ingredient = ingredient_service.update(ingredient_id, data)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Zutat nicht gefunden")
    return ingredient


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: str):
    if not ingredient_service.delete(ingredient_id):
        raise HTTPException(status_code=404, detail="Zutat nicht gefunden")
