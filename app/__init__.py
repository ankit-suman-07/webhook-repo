import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from app.extensions import mongo
from app.webhook.routes import webhook


# Flask app
def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    print("MONGO_URI loaded:", app.config["MONGO_URI"])

    mongo.init_app(app)
    
    app.register_blueprint(webhook)
    
    return app

