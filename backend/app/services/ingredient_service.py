"""Business-Logik für CRUD-Operationen auf der Zutaten-Tabelle."""

from datetime import UTC, datetime
from decimal import Decimal

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

from app.db.client import get_table
from app.models.ingredient import (
    Ingredient,
    IngredientCreate,
    IngredientListResponse,
    IngredientUpdate,
)


def _to_dynamo(obj: dict) -> dict:
    """float → Decimal für DynamoDB."""
    import json
    return json.loads(
        json.dumps(obj),
        parse_float=Decimal,
    )


def _from_dynamo(item: dict) -> dict:
    """Decimal → float für Pydantic."""
    import json
    return json.loads(json.dumps(item, default=float))


class IngredientService:
    def __init__(self):
        self.table = get_table()

    # ── Create ──────────────────────────────────────────────────────────────

    def create(self, data: IngredientCreate) -> Ingredient:
        now = datetime.now(UTC).isoformat()
        ingredient = Ingredient(
            **data.model_dump(),
            created_at=now,
            updated_at=now,
        )
        self.table.put_item(
            Item=_to_dynamo(ingredient.model_dump()),
            ConditionExpression=Attr("id").not_exists(),
        )
        return ingredient

    # ── Read one ────────────────────────────────────────────────────────────

    def get(self, ingredient_id: str) -> Ingredient | None:
        resp = self.table.get_item(Key={"id": ingredient_id})
        item = resp.get("Item")
        return Ingredient(**_from_dynamo(item)) if item else None

    # ── Read list ────────────────────────────────────────────────────────────

    def list(
        self,
        category: str | None = None,
        search: str | None = None,
        last_key: str | None = None,
        limit: int = 50,
    ) -> IngredientListResponse:
        kwargs: dict = {"Limit": limit}

        if last_key:
            kwargs["ExclusiveStartKey"] = {"id": last_key}

        filter_parts = []
        if category:
            filter_parts.append(Attr("category").eq(category))
        if search:
            filter_parts.append(
                Attr("name").contains(search) | Attr("name_en").contains(search)
            )

        if filter_parts:
            expr = filter_parts[0]
            for part in filter_parts[1:]:
                expr = expr & part
            kwargs["FilterExpression"] = expr

        resp = self.table.scan(**kwargs)
        items = [Ingredient(**_from_dynamo(i)) for i in resp.get("Items", [])]

        return IngredientListResponse(
            items=sorted(items, key=lambda x: x.name),
            total=len(items),
            last_evaluated_key=resp.get("LastEvaluatedKey", {}).get("id"),
        )

    # ── Update (PATCH) ───────────────────────────────────────────────────────

    def update(self, ingredient_id: str, data: IngredientUpdate) -> Ingredient | None:
        existing = self.get(ingredient_id)
        if not existing:
            return None

        updated = existing.model_copy(
            update={k: v for k, v in data.model_dump(exclude_none=True).items()}
        )
        updated.updated_at = datetime.now(UTC).isoformat()

        self.table.put_item(Item=_to_dynamo(updated.model_dump()))
        return updated

    # ── Delete ───────────────────────────────────────────────────────────────

    def delete(self, ingredient_id: str) -> bool:
        try:
            self.table.delete_item(
                Key={"id": ingredient_id},
                ConditionExpression=Attr("id").exists(),
            )
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return False
            raise


ingredient_service = IngredientService()
