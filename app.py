from flask import *
from flask_sqlalchemy import SQLAlchemy
import urllib.parse as urlparse
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = urlparse.urlparse(os.environ["DATABASE_URL"])
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

db.create_all()

@app.route('/fires', methods=['GET', 'POST'])
def fires():
    if request.method == 'POST':
        return report_fire()
    else:
        return find_fires()

def report_fire():
    print(request.json)
    report = request.json

    db.session.add(FireReport(lat = report['location']['latitude'], lon = report['location']['longitude'], device_id = report['device_id'], timestamp = report['time']))
    db.session.commit()
    return ('', 201)

def find_fires():
    reports = FireReport.query.all()
    return (jsonify(json_list=[r.serialize for r in reports]), 200)