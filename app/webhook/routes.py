from flask import Blueprint, request, jsonify, render_template
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])
def receiver():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)

        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400

        if mongo.db is None:
            print("Mongo not connected")
            return jsonify({"error": "Mongo not connected"}), 500

        result = mongo.db.webhook_events.insert_one(data)
        print("Inserted document ID:", result.inserted_id)

        return jsonify({"message": "Data saved to MongoDB"}), 200

    except Exception as e:
        print("Exception in /receiver:", e)
        return jsonify({"error": str(e)}), 500
