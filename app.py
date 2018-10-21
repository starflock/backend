from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from twilio.twiml.messaging_response import MessagingResponse
import os
from datetime import date, timedelta
import pytz
import time
import re
import requests
import pyrebase
import firebase_admin

api_key = os.environ["API_KEY"]
auth_domain = os.environ["AUTH_DOMAIN"]
database_endpoint = os.environ["DATABASE_ENDPOINT"]
project_id = os.environ["PROJECT_ID"]
messaging_sender_id = os.environ["MESSAGING_SENDER_ID"]

config = {
    "apiKey": api_key,
    "authDomain": auth_domain,
    "databaseURL": database_endpoint,
    "projectId": project_id,
    "storageBucket": "",
    "messagingSenderId": messaging_sender_id
}

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db.create_all()


class FireReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(80))
    lon = db.Column(db.String(80))
    device_id = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        return {
            "id": self.id,
            "lat": self.lat,
            "lon": self.lon,
            "device_id": self.device_id,
            "timestamp": self.timestamp
        }


# db.create_all()

@app.route("/fires", methods=["GET", "POST"])
def fires():
    if request.method == "POST":
        return report_fire()
    else:
        return find_fires()


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    resp = MessagingResponse()
    try:
        url = request.values.get("MediaUrl0", None)
        device_id = request.values.get("From", None)
        r = requests.get(url)
        vcard = r.text
        lat = re.search("ll=(.*?),", vcard)
        lon = re.search(",(.*?)&", vcard)
        device_id = device_id
        report = report_meta(lat.group(1).replace("\\", ""), lon.group(1), device_id)
        add_to_disaster_db(fire_report_def(report))
        print("Nothing bad happened!")
        resp.message("Thank You For Your disaster response")
    except Exception as ex:
        resp.message("Please share your location")
        print(ex)
        print("something bad happened!")
    return (str(resp), 200)


@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            user_credentials = request.json
            email = user_credentials["email"]
            password = user_credentials["password"]
            user = auth.create_user_with_email_and_password(email=email,
                                                            password=password)
            auth.send_email_verification(user["idToken"])
            return ("", 200)
    except Exception as e:
        print(e)
    return ("", 200)

def report_fire():
    print(request.json)
    report = request.json
    add_to_disaster_db(fire_report_def(report))
    return ("", 201)


def find_fires():
    yesterday = date.today() - timedelta(1)
    reports = FireReport.query.filter(FireReport.timestamp >= yesterday)
    return (jsonify(json_list=[r.serialize for r in reports]), 200)


def fire_report_def(report):
    return FireReport(
        lat=report["location"]["latitude"],
        lon=report["location"]["longitude"],
        device_id=report["device_id"])


def report_meta(lat, lon, device_id):
    meta = {
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "device_id": device_id
    }

    return meta


def add_to_disaster_db(fire_report):
    db.session.add(fire_report)
    db.session.commit()
