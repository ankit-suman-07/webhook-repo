from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415

    event_type = request.headers.get('X-GitHub-Event')
    payload = request.get_json()
    now = datetime.utcnow()
    timestamp_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')  # ISO 8601 UTC format string

    doc = {
        "timestamp": timestamp_str
    }

    if event_type == "push":
        # Extract values
        author = payload.get("pusher", {}).get("name", "unknown")
        to_branch = payload.get("ref", "").split("/")[-1]
        request_id = payload.get("head_commit", {}).get("id", "")  # fallback if not available

        # Populate document
        doc.update({
            "request_id": request_id,
            "author": author,
            "action": "PUSH",
            "from_branch": "",  # Not applicable
            "to_branch": to_branch
        })

    elif event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        author = pr.get("user", {}).get("login", "unknown")
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")
        request_id = str(pr.get("id", ""))

        if action == "opened":
            doc.update({
                "request_id": request_id,
                "author": author,
                "action": "PULL_REQUEST",
                "from_branch": from_branch,
                "to_branch": to_branch
            })

        elif action == "closed" and pr.get("merged"):
            doc.update({
                "request_id": request_id,
                "author": author,
                "action": "MERGE",
                "from_branch": from_branch,
                "to_branch": to_branch
            })
        else:
            return jsonify({"message": "Unhandled pull_request action"}), 204

    else:
        return jsonify({"message": "Unsupported event type"}), 204

    # Insert into MongoDB
    mongo.db.events.insert_one(doc)
    return jsonify({"status": "stored"}), 200
