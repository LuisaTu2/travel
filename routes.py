from flask import Flask, request

from constants import TRAVELS
from db.helpers import build_update_item_request
from models import Photo


def register_routes(app: Flask, db):

    @app.route("/")
    def travel():
        s = "travel the world little bug"
        return f"<p>{s}</p>"

    # curl --header "Content-Type: application/json" -X POST -d '{"pk": "photos", "sk": "beograd:677" , "title": "bazam" , "description" : "thunderstorm"}'  http://localhost:5000/add-photo
    @app.route("/add-photo", methods=["POST"])
    def add_photo():
        photo = Photo.parse_obj(request.get_json())
        db.put_item(TRAVELS, item=photo)
        return f"[r-add-photo] created new photo pk:{photo.pk}, sk: {photo.sk}"

    # curl --header "Content-Type: application/json" -X POST -d '{"pk": "photos", "sk": "beograd:6677"}'  http://localhost:5000/delete-photo
    @app.route("/delete-photo", methods=["POST"])
    def delete_photo():
        photo = Photo.parse_obj(request.get_json())
        db.delete_item(TRAVELS, item=photo)
        return f"[r-delete_photo] deleted photo pk:{photo.pk}, sk: {photo.sk}"

    # TODO: find a way for mačka!
    # TODO: find a way for deleting a comment
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photos", "sk": "beograd:6677"},  "action": "INCREMENT_REACTION", "reaction": "doggo" }'  http://localhost:5000/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photos", "sk": "beograd:6677"}, "action": "ADD_COMMENT", "comment": "cliclicli"}'  http://localhost:5000/update-photo
    # curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"key": {"pk": "photos", "sk": "beograd:6677"}, "action": "DELETE_COMMENT", "position": 0}'  http://localhost:5000/update-photo
    @app.route("/update-photo", methods=["POST"])
    def update_photo():
        data = request.get_json()
        req = build_update_item_request(data)
        db.update_item(TRAVELS, req)
        return f"[r-update-photo] updated photo {req} \n"
