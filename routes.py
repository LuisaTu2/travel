from flask import Flask, request
from boto3.dynamodb.conditions import Key
from constants import PARTITION_KEY, SORT_KEY, TRAVELS, PARTITION_KEY_VALUE

from constants import TRAVELS
import simplejson
from models import Photo, UpdateItemRequest


def register_routes(app: Flask, db):
    @app.route("/api/hello")
    def hello():
        s = "travel the world my little bug"
        return f"<div>{s}</div>"


    @app.route("/api/travel")
    def travel():
        s = "travel the world my little bug"
        image = "https://travels-photos-00.s3.us-east-2.amazonaws.com/beograd:1000"
        return f"<html><div>hello moj beograd! {s} </div><img src='{image}'/></html>"

    # curl -G -d  "pattern=beograd" http://localhost:5000/get-photos
    @app.route("/api/get-photos", methods=["GET"])
    def get_photos():
        try:
            pattern = request.args.get("pattern")
            table = db.get_table(TRAVELS)
            items = table.query(
                ProjectionExpression="pk, sk, title, description, link, comments, reactions",
                KeyConditionExpression=Key(PARTITION_KEY).eq(PARTITION_KEY_VALUE)
                & Key(SORT_KEY).begins_with(pattern),
            )["Items"]

            photos = [
                dict(
                    Photo(
                        pk=item["pk"],
                        sk=item["sk"],
                        reactions=item["reactions"],
                        title=item["title"],
                        description=item["description"],
                        link=item["link"],
                        comments=item["comments"],
                    )
                )
                for item in items
            ]
            res = simplejson.dumps({"photos": photos}, use_decimal=True)
        except Exception as e:
            raise Exception(f"[get_photos] could not retrieve photos \n {e}")
        else:
            return res

    # TODO: find a way for mačka!
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:04000"}, "reaction": "doggo" }'  http://localhost:5000/api/update-photo

    # TODO: maybe allow comments one day!
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:4000"}, "action": "INCREMENT_REACTION", "reaction": "doggo" }'  http://localhost:5000/api/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:4000"}, "action": "ADD_COMMENT", "comment": "cliclicli"}'  http://localhost:5000/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:4000"}, "action": "DELETE_COMMENT", "position": 0}'  http://localhost:5000/update-photo
    @app.route("/api/update-photo", methods=["POST"])
    def update_photo():
        # remote_address = request.remote_addr
        real_ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        data = request.get_json()
        reaction = data["reaction"]
        update_expression = "SET reactions.#reaction.likes = reactions.#reaction.likes + :count, reactions.#reaction.liked_by.#ip_address = :temp"
        expression_attribute_names = {"#reaction": f"{reaction}", "#ip_address" : f"{real_ip_addr}"}
        expression_attribute_values = {":count": int("1"), ":temp": ""}
        req = UpdateItemRequest(
            key=dict(data["key"]),
            update_expression=update_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
        )

        db.update_item(TRAVELS, req)

        return f"[r-update-photo] updated photo {req} \n"



    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:02000"}, "reaction": "sun", "ip_address" : "127.0.0.1" }'  http://localhost:5000/api/delete-reaction
    @app.route("/api/delete-reaction", methods=["POST"])
    def delete_reaction():
        # remote_address = request.remote_addr
        real_ip_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        data = request.get_json()
        reaction = data["reaction"]
        ip_address = data["ip_address"]
        if ip_address != real_ip_addr:
            print("CHECK SOMETHING HERE")

        update_expression = "SET reactions.#reaction.likes = reactions.#reaction.likes - :count REMOVE reactions.#reaction.liked_by.#ip_address"
        expression_attribute_names = {"#reaction": f"{reaction}", "#ip_address" : f"{real_ip_addr}"}
        expression_attribute_values = {":count": int("1")}
        req = UpdateItemRequest(
            key=dict(data["key"]),
            update_expression=update_expression,
            expression_attribute_names=expression_attribute_names,
            expression_attribute_values=expression_attribute_values,
        )
        db.update_item(TRAVELS, req)

        return f"[r-update-photo] removed reaction {req} \n"
