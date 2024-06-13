from models import Action, UpdateItemRequest, UpdatePhotoRequest


def build_update_item_request(data: dict):
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
