from flask import Flask
from models.photos import Item
from constants import TABLE_NAME
from db import put_item, delete_item, update_reaction


app = Flask(__name__)

# initialize db connection and create table
# create_table("photos")
# delete_table("photos")


@app.route("/")
def travel():
    s = "travel the world little bug"
    return f"<p>{s}</p>"


@app.route("/add-photo")
def add_photo():
    title = "doggo & curtains"
    description = "hot day for a cute doggo"
    partition_key = "photos"
    city = "beograd"
    counter = "3000"
    sort_key = city + "#" + counter
    photo = Item(
        pk=partition_key,
        sk=sort_key,
        title=title,
        description=description,
        likes=5,
        doggo=3,
    )
    put_item(TABLE_NAME, dict(photo))
    return "created a new photo"


@app.route("/delete-photo")
def delete_photo():
    delete_item(TABLE_NAME, "photos", "beograd#2000")
    return "deleted photo"


@app.route("/add-reaction")
def add_reaction():
    update_reaction(TABLE_NAME, "photos", "beograd#2000", "likes")
    update_reaction(TABLE_NAME, "photos", "beograd#3000", "doggo")
    return f"incremented reactions"
