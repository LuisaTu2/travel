import boto3
from botocore.exceptions import ClientError

from constants import DYNAMODB
from models import CreateTableRequest, Item, Photo, UpdateItemRequest


class DynamoDBManager:
    def __init__(self) -> None:
        self.client = boto3.client(DYNAMODB, region_name="us-east-2")
        self.db = boto3.resource(DYNAMODB, region_name="us-east-2")

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
            table = self.db.Table(table_name)
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
        except ClientError as e:
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
            table.update_item(
                Key=request.key,
                UpdateExpression=request.update_expression,
                ExpressionAttributeNames=request.expression_attribute_names,
                ExpressionAttributeValues=request.expression_attribute_values,
            )
        except Exception as e:
            raise Exception(
                f"[update_reaction] could not update attribute for item {request.key} \n {e}"
            )
