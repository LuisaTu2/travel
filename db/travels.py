from constants import PARTITION_KEY, SORT_KEY, TRAVELS
from db.ddb_manager import DynamoDBManager
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

    def create_travels_table(self):
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
