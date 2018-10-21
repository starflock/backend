# NASA Space Apps Challenge hackathon
# backend
The backend for Star Flock's spot that fire app.

## Running locally

```
pip3 install -r requirements.txt
export DATABASE_URL='sqlite:///tmp/reports.db'
export FLASK_APP=app.py
gunicorn app:app
```
