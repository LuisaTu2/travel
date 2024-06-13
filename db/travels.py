from botocore.exceptions import ClientError

from constants import PARTITION_KEY, SORT_KEY, TRAVELS
from db.dynamodb import DynamoDBManager
from models import (
    Action,
    AttributeDefinition,
    AttributeType,
    BillingMode,
    CreateTableRequest,
    KeySchemaElement,
    KeyType,
    UpdateItemRequest,
    UpdatePhotoRequest,
)


class Travels(DynamoDBManager):
    def create_travels_table(self):
        try:
            request = CreateTableRequest(
                attribute_definitions=[
                    AttributeDefinition(
                        AttributeName=PARTITION_KEY, AttributeType=AttributeType.S
                    ),
                    AttributeDefinition(
                        AttributeName=SORT_KEY, AttributeType=AttributeType.S
                    ),
                ],
                table_name=TRAVELS,
                key_schema=[
                    KeySchemaElement(
                        AttributeName=PARTITION_KEY, KeyType=KeyType.HASH.value
                    ),
                    KeySchemaElement(
                        AttributeName=SORT_KEY, KeyType=KeyType.RANGE.value
                    ),
                ],
                billing_mode=BillingMode.PAY_PER_REQUEST,
            )
            self.create_table(request)
        except ClientError as e:
            raise Exception(
                f"[create_travels_table] could not create {TRAVELS} table db \n {e}"
            )

    def build_update_item_request(self, data: dict):
        update_data = UpdatePhotoRequest.parse_obj(data)
        action = update_data.action
        update_expression = ""
        expression_attribute_values = None
        expression_attribute_names = None
        match action:
            case Action.INCREMENT_REACTION:
                update_expression = "SET reactions.#r = reactions.#r + :count"
                expression_attribute_names = {"#r": f"{update_data.reaction.value}"}
                expression_attribute_values = {":count": int("1")}
            case Action.ADD_COMMENT:
                update_expression = "SET comments = list_append(comments, :comment)"
                expression_attribute_values = {":comment": [update_data.comment]}
            case Action.DELETE_COMMENT:
                update_expression = f"REMOVE comments[{update_data.position}]"

        request = UpdateItemRequest(
            key=dict(update_data.key),
            update_expression=update_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
        )
        return request
