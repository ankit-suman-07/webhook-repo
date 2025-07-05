# 📦 GitHub Webhook Receiver

A Flask-based application that captures **GitHub Webhook Events** (`PUSH`, `PULL_REQUEST`, `MERGE`) and stores them in **MongoDB**. A simple UI polls the backend every 15 seconds and displays recent events in a human-readable format.

---

## 🚀 Live Demo

- 🔗 **Frontend/UI:**  
  [https://webhook-repo-kwo9.onrender.com/webhook/](https://webhook-repo-kwo9.onrender.com/webhook/)

- 🔗 **Webhook Endpoint:**  
  `POST https://webhook-repo-kwo9.onrender.com/webhook/receiver`

- 🔗 **Get Events (JSON API):**  
  `GET https://webhook-repo-kwo9.onrender.com/webhook/events`

- 📂 **GitHub Source Repo Triggering Webhooks:**  
  [action-repo](https://github.com/ankit-suman-07/action-repo)

---

## 🧠 Webhook Event Format (Stored in MongoDB)

Each webhook event is stored using the following schema:

```json
{
  "request_id": "commit-or-pr-id",
  "author": "GitHub username",
  "action": "PUSH | PULL_REQUEST | MERGE",
  "from_branch": "source-branch (for PRs or merges)",
  "to_branch": "target-branch",
  "timestamp": "ISO 8601 timestamp",
  "message": "Human-readable description"
}
```
***

## 🗂️ MongoDB Collection Schema

| Field         | Datatype       | Details                                                                |
|---------------|-----------------|------------------------------------------------------------------------|
| `_id`         | `ObjectID`      | MongoDB default ID                                                     |
| `request_id`  | `string`        | Use the Git commit hash directly. For Pull Requests, use the PR ID     |
| `author`      | `string`        | Name of the GitHub user making that action                             |
| `action`      | `string`        | Name of the GitHub action: Enum of `["PUSH", "PULL_REQUEST", "MERGE"]` |
| `from_branch` | `string`        | Name of the Git branch in LHS (source branch)                          |
| `to_branch`   | `string`        | Name of the Git branch in RHS (target branch)                          |
| `timestamp`   | `string (datetime)` | Must be a datetime formatted string (UTC) for the time of action       |
| `message`     | `string` | Stores the formatted message to be sent to UI                          |

***

## 📜 Message Examples

### PUSH
- **Format:**
  - `{author} pushed to {to_branch} on {timestamp}`

- **Example:**
  - `Travis pushed to staging on 1st April 2021 - 9:30 PM UTC`

### PULL_REQUEST
- **Format:**
  - `{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}`

- **Example:**
  - `Travis submitted a pull request from staging to master on 1st April 2021 - 9:00 AM UTC`

### MERGE
- **Format:**
  - `{author} merged branch {from_branch} to {to_branch} on {timestamp}`

- **Example:**
  - `Travis merged branch dev to master on 2nd April 2021 - 12:00 PM UTC`

***

## 📦 Dependencies
- Flask 
- Flask-Login
- Flask-PyMongo 
- Flask-CORS 
- pymongo 
- Python-dotenv

***

## Setup Locally

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Setup MongoDB URI in .env

```bash
MONGODB_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/dbname
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

*******************