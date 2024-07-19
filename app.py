from flask import Flask, jsonify
from flask_cors import CORS

from commands import register_cli
from db.photos import Photos
from db.travels import Travels
from routes import register_routes

app = Flask(__name__)
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

cors = CORS(app, origins="*")

db = Travels()
photos = Photos()

register_routes(app, db)
register_cli(app, db, photos)
