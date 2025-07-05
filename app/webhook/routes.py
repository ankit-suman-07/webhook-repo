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
    # ISO 8601 UTC format string
    timestamp_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Human-readable version for date string
    def suffix(d):
        return "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")

    def format_pretty_date(dt):
        return dt.strftime(f"%-d{suffix(dt.day)} %B %Y - %-I:%M %p UTC")

    readable_timestamp = format_pretty_date(now)

    doc = {
        "timestamp": timestamp_str
    }

    # PUSH event
    if event_type == "push":
        author = payload.get("pusher", {}).get("name", "unknown")
        to_branch = payload.get("ref", "").split("/")[-1]
        request_id = payload.get("head_commit", {}).get("id", "")

        doc.update({
            "request_id": request_id,
            "author": author,
            "action": "PUSH",
            "from_branch": "",
            "to_branch": to_branch,
            "message": f"\"{author}\" pushed to \"{to_branch}\" on {readable_timestamp}"
        }) # Sample: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC

    # PULL REQUEST event
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
                "to_branch": to_branch,
                "message": f"\"{author}\" submitted a pull request from \"{from_branch}\" to \"{to_branch}\" on {timestamp_str}"
            }) # "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC

        # MERGE event
        elif action == "closed" and pr.get("merged"):
            doc.update({
                "request_id": request_id,
                "author": author,
                "action": "MERGE",
                "from_branch": from_branch,
                "to_branch": to_branch,
                "message": f"\"{author}\" merged branch \"{from_branch}\" to \"{to_branch}\" on {timestamp_str}"
            }) # "Travis" merged branch "dev" to \"master\" on 2nd April 2021 - 12:00 PM UTC
        else:
            return jsonify({"message": "Unhandled pull_request action"}), 204

    else:
        return jsonify({"message": "Unsupported event type"}), 204

    mongo.db.events.insert_one(doc)
    return jsonify({"status": "stored"}), 200

@webhook.route('/', methods=["GET"])
def index():
    return "<h2>WebHook App Using Flask</h2>"

@webhook.route('/events', methods=["GET"])
def get_events():
    events = mongo.db.events.find().sort("timestamp", -1)
    return jsonify([
        {
            "message": event.get("message"),
            "timestamp": event.get("timestamp")
        } for event in events
    ])