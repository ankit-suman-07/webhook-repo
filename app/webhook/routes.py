# app/webhook/routes.py

from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.get_json()
    timestamp = datetime.utcnow()

    doc = {
        "event_type": event_type,
        "timestamp": timestamp
    }

    if event_type == "push":
        doc.update({
            "author": payload.get("pusher", {}).get("name", "unknown"),
            "to_branch": payload.get("ref", "").split("/")[-1],
            "message": f'{payload.get("pusher", {}).get("name")} pushed to {payload.get("ref", "").split("/")[-1]}'
        })

    elif event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        author = pr.get("user", {}).get("login", "unknown")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")

        if action == "opened":
            doc.update({
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "message": f'{author} opened a pull request from {from_branch} to {to_branch}'
            })

        elif action == "closed" and pr.get("merged"):
            doc.update({
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "message": f'{author} merged {from_branch} into {to_branch}'
            })

    mongo.db.events.insert_one(doc)
    return jsonify({"status": "stored"}), 200

@webhook.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@webhook.route('/events', methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort("timestamp", -1).limit(10)
    return jsonify([
        {
            "message": event.get("message"),
            "timestamp": event.get("timestamp")
        } for event in events
    ])
