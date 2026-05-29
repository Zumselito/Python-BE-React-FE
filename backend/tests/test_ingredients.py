"""
Tests für die Ingredients API.
Verwendet moto für DynamoDB-Mock — kein echter AWS-Account nötig.
"""

import pytest
from fastapi.testclient import TestClient
from moto import mock_aws
import boto3
import os

# Vor dem Import von app die Env-Variablen setzen
os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"
os.environ["TABLE_NAME"] = "ingredients-test"
os.environ["ENVIRONMENT"] = "test"
# kein DYNAMODB_ENDPOINT → moto übernimmt


@pytest.fixture(scope="function")
def dynamo_table():
    with mock_aws():
        db = boto3.resource("dynamodb", region_name="eu-central-1")
        table = db.create_table(
            TableName="ingredients-test",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()
        yield table


@pytest.fixture
def client(dynamo_table):
    # App nach Fixture-Setup importieren, damit moto aktiv ist
    from app.db import client as db_client
    db_client._resource = None  # Cache leeren

    from app.main import app
    with TestClient(app) as c:
        yield c


SAMPLE_INGREDIENT = {
    "name": "Testkarotte",
    "name_en": "Test Carrot",
    "category": "vegetable",
    "season": ["Sep", "Oct"],
    "tags": ["root", "beta-carotene"],
    "macros": {
        "calories_kcal": 41,
        "protein_g": 0.9,
        "carbs_g": 10.0,
        "sugar_g": 4.7,
        "fat_g": 0.2,
        "saturated_fat_g": 0.0,
        "fiber_g": 2.8,
        "water_g": 88.3,
    },
    "vitamins": {},
    "minerals": {},
    "cooking_effects": [],
}


def test_create_ingredient(client):
    resp = client.post("/api/v1/ingredients/", json=SAMPLE_INGREDIENT)
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Testkarotte"
    assert "id" in data
    assert "created_at" in data


def test_get_ingredient(client):
    create_resp = client.post("/api/v1/ingredients/", json=SAMPLE_INGREDIENT)
    ingredient_id = create_resp.json()["id"]

    resp = client.get(f"/api/v1/ingredients/{ingredient_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Testkarotte"


def test_get_ingredient_not_found(client):
    resp = client.get("/api/v1/ingredients/nonexistent-id")
    assert resp.status_code == 404


def test_list_ingredients(client):
    client.post("/api/v1/ingredients/", json=SAMPLE_INGREDIENT)
    resp = client.get("/api/v1/ingredients/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1
    assert isinstance(data["items"], list)


def test_update_ingredient(client):
    create_resp = client.post("/api/v1/ingredients/", json=SAMPLE_INGREDIENT)
    ingredient_id = create_resp.json()["id"]

    resp = client.patch(
        f"/api/v1/ingredients/{ingredient_id}",
        json={"name": "Geänderte Karotte", "tags": ["updated"]},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "Geänderte Karotte"
    assert resp.json()["tags"] == ["updated"]


def test_delete_ingredient(client):
    create_resp = client.post("/api/v1/ingredients/", json=SAMPLE_INGREDIENT)
    ingredient_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/v1/ingredients/{ingredient_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/api/v1/ingredients/{ingredient_id}")
    assert get_resp.status_code == 404


def test_filter_by_category(client):
    client.post("/api/v1/ingredients/", json=SAMPLE_INGREDIENT)
    resp = client.get("/api/v1/ingredients/?category=vegetable")
    assert resp.status_code == 200
    for item in resp.json()["items"]:
        assert item["category"] == "vegetable"
