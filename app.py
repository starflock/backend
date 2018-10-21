from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from twilio.twiml.messaging_response import MessagingResponse
import os
from datetime import datetime
import pytz
import time
import re
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)
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


db.create_all()

@app.route('/fires', methods=['GET', 'POST'])
def fires():
    if request.method == 'POST':
        return report_fire()
    else:
        return find_fires()


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse()
    try:
        url = request.values.get('MediaUrl0', None)
        device_id = request.values.get('From', None)
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


def report_fire():
    print(request.json)
    report = request.json
    add_to_disaster_db(fire_report_def(report))
    return ('', 201)


def find_fires():
    reports = FireReport.query.all()
    return (jsonify(json_list=[r.serialize for r in reports]), 200)


def fire_report_def(report):
    return FireReport(
        lat=report['location']['latitude'],
        lon=report['location']['longitude'],
        device_id=report['device_id'])


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
