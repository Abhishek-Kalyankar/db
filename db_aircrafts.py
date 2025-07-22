from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://aircraft_data_user:6PZIW63RoeCj5cthsEPTZaCeSZm2ZQEQ@dpg-d1t092emcj7s73b0mhlg-a.oregon-postgres.render.com/aircraft_data"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the model
class AircraftData(db.Model):
    __tablename__ = 'aircraft_data'

    id = db.Column(db.Integer, primary_key=True)
    icao24 = db.Column(db.String(10))
    callsign = db.Column(db.String(10))
    origin_country = db.Column(db.String(50))
    time_position = db.Column(db.BigInteger)
    last_contact = db.Column(db.BigInteger)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    baro_altitude = db.Column(db.Float)
    on_ground = db.Column(db.Boolean)
    velocity = db.Column(db.Float)
    true_track = db.Column(db.Float)
    vertical_rate = db.Column(db.Float)
    geo_altitude = db.Column(db.Float)
    squawk = db.Column(db.String(10))
    spi = db.Column(db.Boolean)
    position_source = db.Column(db.Integer)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return "Aircraft Data from PostgreSQL Database"

@app.route('/db-aircrafts', methods=['GET'])
def get_db_aircrafts():
    aircrafts = AircraftData.query.order_by(AircraftData.recorded_at.desc()).limit(1000).all()
    data = [{
        'icao24': a.icao24,
        'callsign': a.callsign,
        'origin_country': a.origin_country,
        'longitude': a.longitude,
        'latitude': a.latitude,
        'baro_altitude': a.baro_altitude,
        'geo_altitude': a.geo_altitude,
        'velocity': a.velocity,
        'on_ground': a.on_ground
    } for a in aircrafts]
    return jsonify({'source': 'database', 'aircrafts': data})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
