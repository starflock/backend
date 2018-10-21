# NASA Space Apps Challenge hackathon
# backend
The backend for Star Flock's spot that fire app.

## Running locally

```
pip3 install -r requirements.txt
export DATABASE_URL='sqlite:///tmp/reports.db'
export FLASK_APP=app.py
export SECRET_KEY=<secret_key>
export API_KEY=<api_key>
export AUTH_DOMAIN=<auth_domain>
export DATABASE_ENDPOINT=<database_endpoint>
export PROJECT_ID=<project_id>
export MESSAGING_SENDER_ID=<messaging_sender_id>
gunicorn app:app
```
