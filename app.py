from flask import *
from flask_sqlalchemy import SQLAlchemy
from urllib import parse
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = parse(os.environ["DATABASE_URL"])
db = SQLAlchemy(app)

class FireReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(80))
    lon = db.Column(db.String(80))
    device_id = db.Column(db.String(80))
    timestamp = db.Column(db.String(80))

db.create_all()

@app.route('/fires', methods=['GET', 'POST'])
def fires():
    if request.method == 'POST':
        return report_fire()
    else:
        return find_fires()

def report_fire():
    report = request.json

    db.session.add(FireReport(lat = report['location']['latitude'], lon = report['location']['longitude'], device_id = report['device_id'], timestamp = report['timestamp']))
    db.commit()
    return ('', 201)

def find_fires():
    return ('hello', 200)