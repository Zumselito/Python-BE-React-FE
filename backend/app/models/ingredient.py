"""
Datenmodell für eine Zutat mit vollständigen Nährwertdaten.
Alle Angaben per 100g Lebensmittel (Rohgewicht).
"""

from __future__ import annotations

from enum import StrEnum
from uuid import uuid4

from pydantic import BaseModel, Field


# ── Enums ─────────────────────────────────────────────────────────────────────


class FoodCategory(StrEnum):
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    GRAIN = "grain"
    LEGUME = "legume"
    DAIRY = "dairy"
    MEAT = "meat"
    FISH = "fish"
    EGG = "egg"
    NUT_SEED = "nut_seed"
    OIL_FAT = "oil_fat"
    HERB_SPICE = "herb_spice"
    OTHER = "other"


class Unit(StrEnum):
    GRAM = "g"
    MILLIGRAM = "mg"
    MICROGRAM = "µg"


# ── Sub-models ─────────────────────────────────────────────────────────────────


class Macros(BaseModel):
    """Makronährstoffe in Gramm pro 100g."""

    calories_kcal: float = Field(ge=0, description="Kalorien (kcal)")
    protein_g: float = Field(ge=0, description="Protein (g)")
    carbs_g: float = Field(ge=0, description="Kohlenhydrate (g)")
    sugar_g: float = Field(ge=0, description="davon Zucker (g)")
    fat_g: float = Field(ge=0, description="Fett (g)")
    saturated_fat_g: float = Field(ge=0, description="davon gesättigte Fettsäuren (g)")
    fiber_g: float = Field(ge=0, description="Ballaststoffe (g)")
    water_g: float = Field(ge=0, le=100, description="Wassergehalt (g)")


class Vitamins(BaseModel):
    """Vitamine in mg oder µg pro 100g."""

    vitamin_a_µg: float = Field(ge=0, default=0.0, description="Vitamin A (Retinol-Äq., µg)")
    vitamin_b1_mg: float = Field(ge=0, default=0.0, description="Vitamin B1 Thiamin (mg)")
    vitamin_b2_mg: float = Field(ge=0, default=0.0, description="Vitamin B2 Riboflavin (mg)")
    vitamin_b3_mg: float = Field(ge=0, default=0.0, description="Vitamin B3 Niacin (mg)")
    vitamin_b5_mg: float = Field(ge=0, default=0.0, description="Vitamin B5 Pantothensäure (mg)")
    vitamin_b6_mg: float = Field(ge=0, default=0.0, description="Vitamin B6 (mg)")
    vitamin_b7_µg: float = Field(ge=0, default=0.0, description="Vitamin B7 Biotin (µg)")
    vitamin_b9_µg: float = Field(ge=0, default=0.0, description="Vitamin B9 Folat (µg)")
    vitamin_b12_µg: float = Field(ge=0, default=0.0, description="Vitamin B12 (µg)")
    vitamin_c_mg: float = Field(ge=0, default=0.0, description="Vitamin C Ascorbinsäure (mg)")
    vitamin_d_µg: float = Field(ge=0, default=0.0, description="Vitamin D (µg)")
    vitamin_e_mg: float = Field(ge=0, default=0.0, description="Vitamin E Tocopherol (mg)")
    vitamin_k_µg: float = Field(ge=0, default=0.0, description="Vitamin K (µg)")


class Minerals(BaseModel):
    """Mineralstoffe und Spurenelemente in mg oder µg pro 100g."""

    calcium_mg: float = Field(ge=0, default=0.0, description="Calcium (mg)")
    iron_mg: float = Field(ge=0, default=0.0, description="Eisen (mg)")
    magnesium_mg: float = Field(ge=0, default=0.0, description="Magnesium (mg)")
    phosphorus_mg: float = Field(ge=0, default=0.0, description="Phosphor (mg)")
    potassium_mg: float = Field(ge=0, default=0.0, description="Kalium (mg)")
    sodium_mg: float = Field(ge=0, default=0.0, description="Natrium (mg)")
    zinc_mg: float = Field(ge=0, default=0.0, description="Zink (mg)")
    copper_mg: float = Field(ge=0, default=0.0, description="Kupfer (mg)")
    manganese_mg: float = Field(ge=0, default=0.0, description="Mangan (mg)")
    selenium_µg: float = Field(ge=0, default=0.0, description="Selen (µg)")
    iodine_µg: float = Field(ge=0, default=0.0, description="Jod (µg)")
    fluoride_mg: float = Field(ge=0, default=0.0, description="Fluorid (mg)")


class CookingEffect(BaseModel):
    """Veränderung von Nährstoffen durch Garmethode (Faktor 0–1, 1 = kein Verlust)."""

    method: str = Field(description="Garmethode, z.B. 'boiling', 'steaming', 'frying'")
    vitamin_c_retention: float = Field(ge=0, le=1, default=1.0, description="Vitamin-C-Erhalt")
    vitamin_b_retention: float = Field(ge=0, le=1, default=1.0, description="B-Vitamine-Erhalt")
    mineral_retention: float = Field(ge=0, le=1, default=1.0, description="Mineralstoff-Erhalt")
    notes: str = Field(default="", description="Freitext-Hinweis")


# ── Main models ────────────────────────────────────────────────────────────────


class IngredientBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    name_en: str | None = Field(default=None, max_length=200, description="Englischer Name")
    category: FoodCategory
    season: list[str] = Field(default_factory=list, description="Saisonalität, z.B. ['Jun','Jul']")
    tags: list[str] = Field(default_factory=list, description="Freitags-Tags")
    macros: Macros
    vitamins: Vitamins = Field(default_factory=Vitamins)
    minerals: Minerals = Field(default_factory=Minerals)
    cooking_effects: list[CookingEffect] = Field(default_factory=list)
    source: str | None = Field(default=None, description="Datenquelle, z.B. 'BLS 3.02'")
    notes: str | None = Field(default=None, max_length=1000)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    """Alle Felder optional für PATCH-Semantik."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    name_en: str | None = None
    category: FoodCategory | None = None
    season: list[str] | None = None
    tags: list[str] | None = None
    macros: Macros | None = None
    vitamins: Vitamins | None = None
    minerals: Minerals | None = None
    cooking_effects: list[CookingEffect] | None = None
    source: str | None = None
    notes: str | None = None


class Ingredient(IngredientBase):
    """Vollständige Zutat wie in DynamoDB gespeichert."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: str = Field(description="ISO-8601 UTC")
    updated_at: str = Field(description="ISO-8601 UTC")


# ── List response ──────────────────────────────────────────────────────────────


class IngredientListResponse(BaseModel):
    items: list[Ingredient]
    total: int
    last_evaluated_key: str | None = None  # für DynamoDB Pagination
