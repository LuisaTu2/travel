import boto3
from mypy_boto3_dynamodb.client import DynamoDBClient
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table

from constants import DYNAMODB, PARTITION_KEY, SORT_KEY, TRAVELS
from models import (
    AttributeDefinition,
    AttributeType,
    BillingMode,
    CreateTableRequest,
    Item,
    KeySchemaElement,
    KeyType,
    Photo,
    UpdateItemRequest,
)

DYNAMO_DB_CLIENT: DynamoDBClient = boto3.client(DYNAMODB)
DYNAMO_DB: DynamoDBServiceResource = boto3.resource(DYNAMODB)


class DatabaseManager:
    def __init__(self) -> None:
        self.client
        self.db

    def init_db(self):
        pass

    def exceptions(self):
        return self.client.exceptions

    def create_table(self, request: CreateTableRequest):
        try:
            self.db.create_table(
                AttributeDefinitions=request.attribute_definitions,
                TableName=request.table_name,
                KeySchema=request.key_schema,
                BillingMode=request.billing_mode,
            )
            print(f"[create_table] created table {request.table_name}")
        except self.exceptions().ResourceInUseException:
            print(f"[create_table] table {request.table_name} already exists")
            pass

        except Exception as e:
            raise Exception(
                f"[create_table] could not create table  in aws.dynamodb \n {e}"
            )

    def get_table(self, table_name: str):
        try:
            table: Table = self.db.Table(table_name)
        except Exception as e:
            raise Exception(f"[get_table] unable to get table {table_name} \n {e}")
        else:
            return table

    def delete_table(self, table_name: str):
        try:
            table = self.get_table(table_name)
            table.delete()
            print(f"[delete_table] deleted table {table_name} \n")
        except self.exceptions().ResourceNotFoundException as e:
            print(f"[delete_table] table {table_name} not found \n {e}")
            pass

    def put_item(self, table_name: str, item: Item | Photo):
        try:
            table = self.get_table(table_name)
            table.put_item(TableName=table_name, Item=dict(item))
        except Exception as e:
            raise Exception(
                f"[add_photo] could not add photo {item} to table {table_name} \n {e}"
            )

    def delete_item(self, table_name: str, item: Item):
        try:
            table = self.get_table(table_name)
            table.delete_item(TableName=table_name, Key={"pk": item.pk, "sk": item.sk})
        except Exception as e:
            raise Exception(
                f"[delete_item] could not delete photo {item.pk, item.sk} from table {table_name} \n {e}"
            )

    def update_item(self, table_name: str, request: UpdateItemRequest):
        try:
            table = self.get_table(table_name)
            if (
                request.expression_attribute_values
                and request.expression_attribute_names
            ):
                table.update_item(
                    Key=request.key,
                    UpdateExpression=request.update_expression,
                    ExpressionAttributeNames=request.expression_attribute_names,
                    ExpressionAttributeValues=request.expression_attribute_values,
                )
            elif (
                request.expression_attribute_values
                and not request.expression_attribute_names
            ):
                table.update_item(
                    Key=request.key,
                    UpdateExpression=request.update_expression,
                    ExpressionAttributeValues=request.expression_attribute_values,
                )
            else:
                table.update_item(
                    Key=request.key,
                    UpdateExpression=request.update_expression,
                )
        except Exception as e:
            raise Exception(
                f"[update_reaction] could not update attribute for item {request.key} \n {e}"
            )


class DynamoDB(DatabaseManager):
    def __init__(self) -> None:
        self.client = DYNAMO_DB_CLIENT
        self.db = DYNAMO_DB

    def build_create_table_request(
        self,
        attribute_definitions,
        table_name: str,
        key_schema_elements,
        billing_mode: str,
    ):
        attribute_definitions = [
            AttributeDefinition(AttributeName=attribute[0], AttributeType=attribute[1])
            for attribute in attribute_definitions
        ]
        key_schema_elements = [
            KeySchemaElement(AttributeName=element[0], KeyType=element[1])
            for element in key_schema_elements
        ]
        return CreateTableRequest(
            attribute_definitions=attribute_definitions,
            table_name=table_name,
            key_schema=key_schema_elements,
            billing_mode=billing_mode,
        )

    def create_travel_table(self):
        try:
            request = self.build_create_table_request(
                attribute_definitions=[
                    (PARTITION_KEY, AttributeType.S),
                    (SORT_KEY, AttributeType.S),
                ],
                table_name=TRAVELS,
                key_schema_elements=[
                    (PARTITION_KEY, KeyType.HASH.value),
                    (SORT_KEY, KeyType.RANGE.value),
                ],
                billing_mode=BillingMode.PAY_PER_REQUEST,
            )
            self.create_table(request)
        except Exception as e:
            raise Exception(
                f"[create_travel_table] could not create travel table db \n {e}"
            )
