from flask import Flask

from cli import register_cli
from db.photos import Photos
from db.travels import Travels
from routes import register_routes

app = Flask(__name__)

db = Travels()
photos = Photos()

register_routes(app, db)
register_cli(app, db, photos)
