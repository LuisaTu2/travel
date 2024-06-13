from flask import Flask, request

from constants import TRAVELS


def register_routes(app: Flask, db):
    @app.route("/")
    def travel():
        s = "travel the world little bug"
        return f"<div><p>{s}</p><img src='https://travels-photos-00.s3.us-east-2.amazonaws.com/beograd:1000'></div>"

    # TODO: find a way for mačka!
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photos", "sk": "beograd:6677"},  "action": "INCREMENT_REACTION", "reaction": "doggo" }'  http://localhost:5000/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photos", "sk": "beograd:6677"}, "action": "ADD_COMMENT", "comment": "cliclicli"}'  http://localhost:5000/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photos", "sk": "beograd:6677"}, "action": "DELETE_COMMENT", "position": 0}'  http://localhost:5000/update-photo
    @app.route("/update-photo", methods=["POST"])
    def update_photo():
        data = request.get_json()
        req = db.build_update_item_request(data)
        db.update_item(TRAVELS, req)
        return f"[r-update-photo] updated photo {req} \n"
