from flask import Flask
from dynamodb import *


app = Flask(__name__)

# initialize db connection and create table
# create_table("photos")
# delete_table("photos")


@app.route("/")
def travel():
    s = "travel the world little bug"
    return f"<p>{s}</p>"


@app.route("/create-photo")
def create_photo():
    # add_photo("title 2", "another description")
    return "created a new photo"
