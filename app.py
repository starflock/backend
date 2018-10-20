from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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


class FireReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(80))
    lon = db.Column(db.String(80))
    device_id = db.Column(db.String(80))
    timestamp = db.Column(db.String(80))

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

@app.route('/fires', methods=['GET', 'POST'])
def fires():
    if request.method == 'POST':
        return report_fire()
    else:
        return find_fires()


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    url = request.values.get('MediaUrl0', None)
    r = requests.get(url)
    vcard = r.text

    device_id = request.values.get('from', None)
    print(vcard)
    print(device_id)
    if vcard is not None:
        lat = re.search("ll=(.*?)\\,", vcard)
        lon = re.search(",(.*?)&", vcard)
        device_id = device_id
        timestamp = get_time_stamp_tz()
        resp = MessagingResponse()
        if lat is not None and lon is not None:
            report = report_meta(lat.group(1), lon.group(1), device_id, timestamp)
            print(fire_report_def(report))
            add_to_disaster_db(fire_report_def(report))
            resp.message("Thank You For Your disaster response")
        else:
            print("something bad happened!")
            resp.message("Please share your location")

    return ('', 200)


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
        device_id=report['device_id'],
        timestamp=report['time'])


def report_meta(lat, lon, device_id, time):
    meta = {
        "location": {
            "latitude": lat,
            "longitude": lon
        },
        "device_id": device_id,
        "time": time
    }

    return meta


def get_time_stamp_tz():
    time_stamp = int(round(time.time() * 1000))
    return datetime.fromtimestamp(float(time_stamp) / 1000, tz=pytz.UTC).isoformat()


def add_to_disaster_db(fire_report):
    db.session.add(fire_report)
    db.session.commit()
