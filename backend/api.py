from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restful import Resource, Api, marshal_with, fields, reqparse
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
import datetime


app = Flask(__name__)
api = Api(app)
CORS(app)
#, supports_credentials=True
CORS(app, resources={r"/*": {"origins": "*"}})
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

class MeasurementModel(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    heartrate = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    mood = db.Column(db.String)
    sound = db.Column(db.Integer)
    date = db.Column(db.String)
    time = db.Column(db.String)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))

MeasurementModelMarshal = {
    'id': fields.Integer,
    'distance': fields.Integer,
    'heartrate': fields.Integer,
    'amount': fields.Integer,
    'mood': fields.String, 
    'sound': fields.Integer,
    'date': fields.String,
    'time': fields.String,
    'sensor_id': fields.Integer
}

class roomModel(db.Model):
    
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

RoomModelMarshal = {
    'id': fields.Integer,
    'name': fields.Integer
}

class sensorModel(db.Model):

    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

SensorModelMarshal = {
    'id': fields.Integer,
    'name': fields.Integer,
    'room_id': fields.Integer
}

class testModel(db.Model):
    
    __tablename__ = 'test'
    test = db.Column(db.String, primary_key=True)

TestModelMarshal = {
    'test': fields.String
}

@app.route("/demo", methods=["POST"])
def demo():
    input_json = request.get_json(force=True)
    test = input_json['test']
    data = testModel(
        test=test
    )
    db.session.add(data)
    db.session.commit()
    return 'succes', 200

#get request laatse endpoint opsturen
# zodat het naar unity kan opgestuurd kan worden

class Measurement(Resource):


    @marshal_with(MeasurementModelMarshal)
    def get(self):
        #where today
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        #distance = DistanceModel.query.filter_by(date=date).all()
        distance = MeasurementModel.query.all()
        return distance

    @marshal_with(MeasurementModelMarshal)
    def post(self):
        data = request.get_json(force=True)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")


        measurementmodel = MeasurementModel()
        measurementmodel.distance = data['distance']
        measurementmodel.sound = data['sound']
        measurementmodel.date = date
        measurementmodel.time = time
        
        db.session.add(measurementmodel)
        db.session.commit()

        return {
            'data': data
            }

api.add_resource(Measurement, '/distance')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=2000, debug=True)