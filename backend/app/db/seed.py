"""
Seed-Skript: Befüllt DynamoDB mit Beispiel-Zutaten.
Aufruf: python -m app.db.seed [--force-recreate]
"""

import argparse
import json
import sys
from datetime import UTC, datetime

from app.db.client import get_dynamodb, get_table, settings
from botocore.exceptions import ClientError

NOW = datetime.now(UTC).isoformat()

SAMPLE_INGREDIENTS = [
    {
        "id": "broccoli-001",
        "name": "Brokkoli",
        "name_en": "Broccoli",
        "category": "vegetable",
        "season": ["Jun", "Jul", "Aug", "Sep", "Oct"],
        "tags": ["cruciferous", "high-fiber", "antioxidant"],
        "macros": {
            "calories_kcal": 34,
            "protein_g": 2.8,
            "carbs_g": 4.0,
            "sugar_g": 1.7,
            "fat_g": 0.4,
            "saturated_fat_g": 0.1,
            "fiber_g": 2.6,
            "water_g": 89.3,
        },
        "vitamins": {
            "vitamin_a_µg": 31,
            "vitamin_b1_mg": 0.07,
            "vitamin_b2_mg": 0.12,
            "vitamin_b3_mg": 0.64,
            "vitamin_b5_mg": 0.57,
            "vitamin_b6_mg": 0.19,
            "vitamin_b7_µg": 1.8,
            "vitamin_b9_µg": 63,
            "vitamin_b12_µg": 0,
            "vitamin_c_mg": 89.2,
            "vitamin_d_µg": 0,
            "vitamin_e_mg": 0.78,
            "vitamin_k_µg": 101.6,
        },
        "minerals": {
            "calcium_mg": 47,
            "iron_mg": 0.73,
            "magnesium_mg": 21,
            "phosphorus_mg": 66,
            "potassium_mg": 316,
            "sodium_mg": 33,
            "zinc_mg": 0.41,
            "copper_mg": 0.05,
            "manganese_mg": 0.21,
            "selenium_µg": 2.5,
            "iodine_µg": 7,
            "fluoride_mg": 0.01,
        },
        "cooking_effects": [
            {
                "method": "boiling",
                "vitamin_c_retention": 0.55,
                "vitamin_b_retention": 0.65,
                "mineral_retention": 0.70,
                "notes": "Vitamin C geht stark ins Kochwasser über",
            },
            {
                "method": "steaming",
                "vitamin_c_retention": 0.83,
                "vitamin_b_retention": 0.85,
                "mineral_retention": 0.92,
                "notes": "Schonendste Methode für wasserlösliche Vitamine",
            },
            {
                "method": "microwaving",
                "vitamin_c_retention": 0.74,
                "vitamin_b_retention": 0.78,
                "mineral_retention": 0.88,
                "notes": "Kurze Garzeit schont Nährstoffe",
            },
        ],
        "source": "BLS 3.02 / USDA SR28",
        "notes": "Einer der nährstoffreichsten Gemüse; Sulforaphan als bioaktiver Wirkstoff",
        "created_at": NOW,
        "updated_at": NOW,
    },
    {
        "id": "spinach-001",
        "name": "Blattspinat",
        "name_en": "Spinach",
        "category": "vegetable",
        "season": ["Mar", "Apr", "May", "Sep", "Oct"],
        "tags": ["iron-rich", "folate", "leafy-green"],
        "macros": {
            "calories_kcal": 23,
            "protein_g": 2.9,
            "carbs_g": 1.4,
            "sugar_g": 0.4,
            "fat_g": 0.4,
            "saturated_fat_g": 0.1,
            "fiber_g": 2.2,
            "water_g": 91.4,
        },
        "vitamins": {
            "vitamin_a_µg": 469,
            "vitamin_b1_mg": 0.08,
            "vitamin_b2_mg": 0.19,
            "vitamin_b3_mg": 0.72,
            "vitamin_b5_mg": 0.07,
            "vitamin_b6_mg": 0.20,
            "vitamin_b7_µg": 6.9,
            "vitamin_b9_µg": 194,
            "vitamin_b12_µg": 0,
            "vitamin_c_mg": 28.1,
            "vitamin_d_µg": 0,
            "vitamin_e_mg": 2.03,
            "vitamin_k_µg": 483,
        },
        "minerals": {
            "calcium_mg": 99,
            "iron_mg": 2.71,
            "magnesium_mg": 79,
            "phosphorus_mg": 49,
            "potassium_mg": 558,
            "sodium_mg": 79,
            "zinc_mg": 0.53,
            "copper_mg": 0.13,
            "manganese_mg": 0.90,
            "selenium_µg": 1.0,
            "iodine_µg": 12,
            "fluoride_mg": 0.03,
        },
        "cooking_effects": [
            {
                "method": "boiling",
                "vitamin_c_retention": 0.50,
                "vitamin_b_retention": 0.60,
                "mineral_retention": 0.65,
                "notes": "Oxalsäure-Gehalt wird durch Kochen reduziert",
            },
            {
                "method": "steaming",
                "vitamin_c_retention": 0.78,
                "vitamin_b_retention": 0.80,
                "mineral_retention": 0.88,
                "notes": "Eisenaufnahme durch Vitamin C verbessern",
            },
        ],
        "source": "BLS 3.02",
        "notes": "Oxalsäure hemmt Eisenaufnahme; Kombination mit Vitamin C verbessert Bioverfügbarkeit",
        "created_at": NOW,
        "updated_at": NOW,
    },
    {
        "id": "salmon-001",
        "name": "Atlantischer Lachs",
        "name_en": "Atlantic Salmon",
        "category": "fish",
        "season": [],
        "tags": ["omega-3", "high-protein", "vitamin-d"],
        "macros": {
            "calories_kcal": 208,
            "protein_g": 20.0,
            "carbs_g": 0.0,
            "sugar_g": 0.0,
            "fat_g": 13.4,
            "saturated_fat_g": 3.1,
            "fiber_g": 0.0,
            "water_g": 64.9,
        },
        "vitamins": {
            "vitamin_a_µg": 12,
            "vitamin_b1_mg": 0.23,
            "vitamin_b2_mg": 0.38,
            "vitamin_b3_mg": 8.69,
            "vitamin_b5_mg": 1.66,
            "vitamin_b6_mg": 0.82,
            "vitamin_b7_µg": 5.0,
            "vitamin_b9_µg": 25,
            "vitamin_b12_µg": 3.18,
            "vitamin_c_mg": 0,
            "vitamin_d_µg": 11.1,
            "vitamin_e_mg": 3.55,
            "vitamin_k_µg": 0.5,
        },
        "minerals": {
            "calcium_mg": 12,
            "iron_mg": 0.34,
            "magnesium_mg": 27,
            "phosphorus_mg": 252,
            "potassium_mg": 384,
            "sodium_mg": 59,
            "zinc_mg": 0.36,
            "copper_mg": 0.25,
            "manganese_mg": 0.02,
            "selenium_µg": 41.4,
            "iodine_µg": 10,
            "fluoride_mg": 0.08,
        },
        "cooking_effects": [
            {
                "method": "baking",
                "vitamin_c_retention": 1.0,
                "vitamin_b_retention": 0.80,
                "mineral_retention": 0.95,
                "notes": "Omega-3-Fettsäuren bei > 200°C leicht reduziert",
            },
            {
                "method": "steaming",
                "vitamin_c_retention": 1.0,
                "vitamin_b_retention": 0.88,
                "mineral_retention": 0.97,
                "notes": "Schonendste Methode; Omega-3 gut erhalten",
            },
        ],
        "source": "USDA SR28",
        "notes": "Exzellente Quelle für EPA/DHA Omega-3; hoher Selen-Gehalt",
        "created_at": NOW,
        "updated_at": NOW,
    },
]


def seed(force_recreate: bool = False) -> None:
    table = get_table()

    if force_recreate:
        # Alle bestehenden Items löschen
        scan = table.scan(ProjectionExpression="id")
        for item in scan.get("Items", []):
            table.delete_item(Key={"id": item["id"]})
        print(f"  Bestehende Items gelöscht")

    for ingredient in SAMPLE_INGREDIENTS:
        table.put_item(Item=ingredient)
        print(f"  ✓ {ingredient['name']} geseedert")

    print(f"\nSeed abgeschlossen: {len(SAMPLE_INGREDIENTS)} Zutaten")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-recreate", action="store_true")
    args = parser.parse_args()
    seed(force_recreate=args.force_recreate)
