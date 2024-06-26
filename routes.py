from flask import Flask, request
from boto3.dynamodb.conditions import Key
from constants import PARTITION_KEY, SORT_KEY, TRAVELS, PARTITION_KEY_VALUE

from constants import TRAVELS
import json
from models import Photo, Reactions


def register_routes(app: Flask, db):
    @app.route("/")
    def travel():
        s = "travel the world my little bug"
        image = "https://travels-photos-00.s3.us-east-2.amazonaws.com/beograd:1000"
        return f"<html><div>hello moj beograd! {s} </div><img src='{image}'/></html>"

    # curl -G -d  "pattern=beograd" http://localhost:5000/get-photos
    @app.route("/get-photos", methods=["GET"])
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
                        reactions=dict(
                            Reactions(
                                doggo=item["reactions"]["doggo"],
                                like=item["reactions"]["like"],
                                macka=item["reactions"]["macka"],
                            )
                        ),
                        title=item["title"],
                        description=item["description"],
                        link=item["link"],
                        comments=item["comments"],
                    )
                )
                for item in items
            ]

            res = json.dumps({"photos": photos})
        except Exception as e:
            raise Exception(f"[get_photos] could not retrieve photos \n {e}")
        else:
            return res
        
    # TODO: find a way for mačka!
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:4000"}, "action": "INCREMENT_REACTION", "reaction": "doggo" }'  http://localhost:5000/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:4000"}, "action": "ADD_COMMENT", "comment": "cliclicli"}'  http://localhost:5000/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photo", "sk": "beograd:4000"}, "action": "DELETE_COMMENT", "position": 0}'  http://localhost:5000/update-photo
    @app.route("/update-photo", methods=["POST"])
    def update_photo():
        data = request.get_json()
        req = db.build_update_item_request(data)
        db.update_item(TRAVELS, req)
        return f"[r-update-photo] updated photo {req} \n"
