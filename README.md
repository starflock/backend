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

**site list**
https://2018.spaceappschallenge.org/challenges/volcanoes-icebergs-and-asteroids-oh-my/real-time-fire-app/teams/starflock/project

![alt text](https://github.com/starflock/backend/blob/master/spotifyre_diagram.png)

[![NASA Space Apps Challenge 2018 - Spotifyre](https://img.youtube.com/vi/K54UmFABUNE/0.jpg)](https://www.youtube.com/watch?v=K54UmFABUNE "NASA Space Apps Challenge 2018 - Spotifyre")
