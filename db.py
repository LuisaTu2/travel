import boto3
from models.photos import KeyType, TableStatus
from constants import BILLING_MODE, DYNAMO_DB


def exceptions():
    return boto3.client(DYNAMO_DB).exceptions


def get_db():
    try:
        db = boto3.resource(DYNAMO_DB)
    except Exception as e:
        raise Exception(f"[get_db] unable to get db, {e}")
    else:
        return db


def create_table(table_name: str):
    try:
        db = get_db()
        db.create_table(
            AttributeDefinitions=[
                {"AttributeName": "pk", "AttributeType": "S"},
                {"AttributeName": "sk", "AttributeType": "S"},
            ],
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "pk", "KeyType": KeyType.HASH},
                {"AttributeName": "sk", "KeyType": KeyType.RANGE},
            ],
            BillingMode=BILLING_MODE,
        )
    except exceptions().ResourceInUseException as e:
        print(f"[create_table] table {table_name} already exists \n {e}")
        pass

    except Exception as e:
        raise Exception(
            f"[create_table] could not create table {table_name} in aws.dynamodb \n {e}"
        )


def get_table(table_name: str):
    try:
        db = get_db()
        table = db.Table(table_name)
    except Exception as e:
        raise Exception(f"[get_table] unable to get table {table_name} \n {e}")
    else:
        return table


def delete_table(table_name: str):
    try:
        table = get_table(table_name)
        table.delete()
    except exceptions().ResourceNotFoundException as e:
        print(f"[delete_table] table {table_name} not found \n {e}")
        pass


def put_item(table_name: str, item: dict):
    try:
        table = get_table(table_name)
        table_status = table.table_status
        if table_status == TableStatus.ACTIVE:
            table.put_item(TableName=table_name, Item=item)
        else:
            raise Exception(
                f"[add_photo] table {table} is not currently active, status: {table_status}"
            )
    except Exception as e:
        raise Exception(f"[add_photo] unable to add photo {item} \n {e}")


def delete_item(table_name: str, pk: str, sk: str):
    try:
        table = get_table(table_name)
        table_status = table.table_status
        if table_status == TableStatus.ACTIVE:
            table.delete_item(TableName=table_name, Key={"pk": pk, "sk": sk})
        else:
            raise Exception(
                f"[add_photo] table {table} is not currently active, status: {table_status}"
            )
    except Exception as e:
        raise Exception(f"[delete_item] unable to delete photo {pk, sk} \n {e}")