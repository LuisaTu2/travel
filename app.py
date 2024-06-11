from flask import Flask, request
from models.photos import Photo
from db import Database


app = Flask(__name__)

db = Database()
# db.create_table(TRAVELS)
# db.delete_table(TRAVELS)


@app.route("/")
def travel():
    s = "travel the world little bug"
    return f"<p>{s}</p>"


# POST WITH JSON
# curl --header "Content-Type: application/json" -X POST -d '{"pk": "photos", "sk": "beograd:2000" , "title": "flower" , "description" : "a pretty flower"}'  http://localhost:5000/add-photo
@app.route("/add-photo", methods=["POST"])
def add_photo():
    photo = Photo.parse_obj(request.get_json())
    db.put_item(item=photo)
    return f"[add_photo] created new photo pk:{photo.pk}, sk: {photo.sk}\n"


# POST WITH JSON
# curl --header "Content-Type: application/json" -X POST -d '{"pk": "photos", "sk": "beograd:2000"}'  http://localhost:5000/delete-photo
@app.route("/delete-photo", methods=["POST"])
def delete_photo():
    photo = Photo.parse_obj(request.get_json())
    db.delete_item(item=photo)
    return f"[delete_photo] deleted photo pk:{photo.pk}, sk: {photo.sk}\n"


# TODO: find a way for mačka!
# curl --header "Content-Type: application/json; Charset='UTF-8'" -X POST -d '{"pk": "photos", "sk": "beograd:2000", "reaction": "likes"}'  http://localhost:5000/add-reaction
@app.route("/add-reaction", methods=["POST"])
def add_reaction():
    data = request.get_json()
    photo = Photo(pk=data["pk"], sk=data["sk"])
    reaction = data["reaction"]
    db.increment_reaction(photo=photo, reaction=reaction)
    return f"[add_reaction] incremented reaction for photo pk:{photo.pk}, sk: {photo.sk}, reaction={reaction}\n"
