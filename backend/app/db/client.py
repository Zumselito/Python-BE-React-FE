"""DynamoDB-Client und Tabellen-Setup."""

import boto3
from botocore.exceptions import ClientError

from app.core.config import settings

_resource: boto3.resource | None = None


def get_dynamodb():
    global _resource
    if _resource is None:
        kwargs: dict = {
            "region_name": settings.aws_default_region,
            "aws_access_key_id": settings.aws_access_key_id,
            "aws_secret_access_key": settings.aws_secret_access_key,
        }
        if settings.dynamodb_endpoint:
            kwargs["endpoint_url"] = settings.dynamodb_endpoint
        _resource = boto3.resource("dynamodb", **kwargs)
    return _resource


def get_table():
    return get_dynamodb().Table(settings.table_name)


async def ensure_table() -> None:
    """Erstellt die Tabelle, falls sie noch nicht existiert (lokal & CI)."""
    db = get_dynamodb()
    try:
        table = db.Table(settings.table_name)
        table.load()
        print(f"✓ Tabelle '{settings.table_name}' bereits vorhanden")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            _create_table(db)
        else:
            raise


def _create_table(db) -> None:
    table = db.create_table(
        TableName=settings.table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()
    print(f"✓ Tabelle '{settings.table_name}' erstellt")
