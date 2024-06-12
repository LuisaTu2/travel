import boto3
from models.photos import KeyType, Photo, Item
from constants import BILLING_MODE


class Database:
    def __init__(self) -> None:
        self.client = boto3.client("dynamodb")
        self.db = boto3.resource("dynamodb")

    def exceptions(self):
        return self.client.exceptions

    def create_table(self, table_name: str):
        try:
            self.db.create_table(
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
            print(f"[create_table] created table {table_name} \n")
        except self.exceptions().ResourceInUseException as e:
            print(f"[create_table] table {table_name} already exists \n {e}")
            pass

        except Exception as e:
            raise Exception(
                f"[create_table] could not create table {table_name} in aws.dynamodb \n {e}"
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

    def put_item(self, item: Item | Photo):
        try:
            table = self.get_table(item.table_name)
            # remove the table name to avoid dups
            item = dict(item)
            table_name = item["table_name"]
            del item["table_name"]
            table.put_item(TableName=table_name, Item=dict(item))
        except Exception as e:
            raise Exception(f"[add_photo] could not add photo {item} \n {e}")

    def delete_item(self, item: Item):
        try:
            table = self.get_table(item.table_name)
            table.delete_item(
                TableName=item.table_name, Key={"pk": item.pk, "sk": item.sk}
            )
        except Exception as e:
            raise Exception(
                f"[delete_item] could not delete photo {item.pk, item.sk} from table {item.table_name} \n {e}"
            )

    def increment_reaction(self, photo: Photo, reaction: str):
        try:
            table = self.get_table(photo.table_name)
            table.update_item(
                Key={"pk": photo.pk, "sk": photo.sk},
                UpdateExpression=f"set {reaction} = {reaction} + :count",
                ExpressionAttributeValues={":count": int("1")},
            )
        except Exception as e:
            raise Exception(
                f"[update_reaction] could not update attribute {reaction} for item {photo.pk, photo.sk} \n {e}"
            )

    def add_comment(self, photo: Photo, comment: str):
        try:
            table = self.get_table(photo.table_name)
            table.update_item(
                Key={"pk": photo.pk, "sk": photo.sk},
                UpdateExpression="set comments = list_append(comments, :comment)",
                ExpressionAttributeValues={":comment": [comment]},
            )
        except Exception as e:
            raise Exception(
                f"[add_comment] could not add comment to photo {photo.pk, photo.sk} \n {e}"
            )

    def delete_comment(self, photo: Photo, position: int):
        try:
            table = self.get_table(photo.table_name)
            table.update_item(
                Key={"pk": photo.pk, "sk": photo.sk},
                UpdateExpression=f"remove comments[{position}]",
            )
        except Exception as e:
            raise Exception(
                f"[delete_comment] could not delete comment from photo {photo.pk, photo.sk} \n {e}"
            )
