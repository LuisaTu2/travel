import click
from flask import Flask

from constants import TRAVELS
from db.db import DynamoDB
from db.helpers import build_update_item_request
from models import Action, Photo, UpdatePhotoRequest
from routes import register_routes
from cli import register_cli


PARTITION_KEY = "pk"
SORT_KEY = "sk"

app = Flask(__name__)

db = DynamoDB()
# db.create_travel_table()
# db.delete_table(TRAVELS)

register_routes(app, db)
register_cli(app, db)
