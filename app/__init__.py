import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from app.extensions import mongo
from app.webhook.routes import webhook


# Creating our flask app
def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    print("MONGO_URI loaded:", app.config["MONGO_URI"])

    mongo.init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)

    @app.route("/test-mongo")
    def test_mongo():
        try:
            print("🔍 Trying to insert into Mongo...")
            mongo.db.test_collection.insert_one({"status": "ok"})
            return jsonify({"status": "Mongo working"}), 200
        except Exception as e:
            print("🔥 Error in /test-mongo:", repr(e))  # ← More detailed error
            return jsonify({"error": str(e)}), 500
    
    return app

