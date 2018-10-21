# NASA Space Apps Challenge hackathon
# backend
The backend for Star Flock's spot that fire app.

## Running locally

```
pip3 install -r requirements.txt
export DATABASE_URL='sqlite:///tmp/reports.db'
export FLASK_APP=app.py
SECRET_KEY=<secret_key>
export apiKey=<api_key>
export authDomain=<auth_domain>
export databaseURL=<database_endpoint>
export projectId=<project_id>
export messagingSenderId=<messaging_sender_id>
gunicorn app:app
```
