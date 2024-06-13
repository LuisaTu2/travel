from flask import Flask

from db.travels import Travels
from routes import register_routes
from cli import register_cli


app = Flask(__name__)

db = Travels()

register_routes(app, db)
register_cli(app, db)
