# Webhook Receiver

- Github repository which automatically sends an event (webhook) on the following
Github actions **("Push", "Pull Request", "Merge")** to a registered endpoint, and store it to
MongoDB.
- The UI will keep pulling data from MongoDB every 15 seconds and display the latest
changes to the repo in the following format:

**Sample Repo:** [action-repo](https://github.com/ankit-suman-07/action-repo)

**Deployed using rendered.com at:** ***https://webhook-repo-kwo9.onrender.com/webhook/events***

### Endpoints - Based on deployed url:

- To save events in MongoDB

```bash
POST http://webhook-repo-kwo9.onrender.com/webhook/receiver
```

- To display saved events

```bash
GET https://webhook-repo-kwo9.onrender.com/webhook/events
```

### For PUSH action:
- **Format:** {author} pushed to {to_branch} on {timestamp}
- **Sample:** "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC

### For PULL_REQUEST action:
- **Format:** {author} submitted a pull request from {from_branch} to {to_branch} on
{timestamp}
- **Sample:** "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM
UTC

### For MERGE action (Brownie Points):
- **Format:** {author} merged branch {from_branch} to {to_branch} on {timestamp}
- **Sample:** "Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC

*******************

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

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

*******************