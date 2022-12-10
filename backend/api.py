from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api, marshal_with, fields, reqparse
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
api = Api(app)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.db')
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
    'name': fields.String
}


class sensorModel(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


SensorModelMarshal = {
    'id': fields.Integer,
    'name': fields.String,
    'room_id': fields.Integer
}


class demoModel(db.Model):
    __tablename__ = 'demo'
    id = db.Column(db.Integer, primary_key=True)
    demo = db.Column(db.String)


DemoModelMarshal = {
    'id': fields.Integer,
    'demo': fields.String
}


@app.route("/demo", methods=["GET"])
def get_demo():
    demo = demoModel.query.order_by(demoModel.id.desc()).first()
    return demo.demo, 200


@app.route("/demo", methods=["POST"])
def post_demo():
    input_json = request.get_json(force=True)
    demo = input_json['test']
    data = demoModel(
        demo=demo
    )
    db.session.add(data)
    db.session.commit()
    return 'succes', 200

# get request laatse endpoint opsturen


class Measurement(Resource):
    @marshal_with(MeasurementModelMarshal)
    def get(self):
        # where today
        #date = datetime.datetime.now().strftime("%Y-%m-%d")
        #distance = DistanceModel.query.filter_by(date=date).all()
        distance = MeasurementModel.query.all()
        return distance

    @marshal_with(MeasurementModelMarshal)
    def post(self):
        data = request.get_json(force=True)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        measurement_model = MeasurementModel()
        measurement_model.distance = data['distance']
        measurement_model.sound = data['sound']
        measurement_model.date = date
        measurement_model.time = time

        db.session.add(measurement_model)
        db.session.commit()

        return measurement_model


class Room(Resource):
    @marshal_with(RoomModelMarshal)
    def get(self):
        room = roomModel.query.all()
        return room

    @marshal_with(RoomModelMarshal)
    def post(self):
        data = request.get_json(force=True)
        room_model = roomModel()
        room_model.name = data['name']
        db.session.add(room_model)
        db.session.commit()

        return room_model

    @marshal_with(RoomModelMarshal)
    def delete(self):
        data = request.get_json(force=True)
        print(data)
        room_model = roomModel.query.filter_by(id=data['id']).first()
        db.session.delete(room_model)
        db.session.commit()

        return room_model

    @marshal_with(RoomModelMarshal)
    def put(self):
        data = request.get_json(force=True)
        room_model = roomModel.query.filter_by(id=data['id']).first()
        room_model.name = data['name']
        db.session.commit()

        return room_model


class Sensor(Resource):
    @marshal_with(SensorModelMarshal)
    def get(self):
        sensor = sensorModel.query.all()
        return sensor

    @marshal_with(SensorModelMarshal)
    def post(self):
        data = request.get_json(force=True)
        sensor_model = sensorModel()
        sensor_model.name = data['name']
        sensor_model.room_id = data['room_id']
        db.session.add(sensor_model)
        db.session.commit()

        return sensor_model

    @marshal_with(SensorModelMarshal)
    def delete(self):
        data = request.get_json(force=True)
        sensor_model = sensorModel.query.filter_by(id=data['id']).first()
        db.session.delete(sensor_model)
        db.session.commit()

        return sensor_model

    @marshal_with(SensorModelMarshal)
    def put(self):
        data = request.get_json(force=True)
        sensor_model = sensorModel.query.filter_by(id=data['id']).first()
        sensor_model.name = data['name']
        sensor_model.room_id = data['room_id']
        db.session.commit()

        return sensor_model


api.add_resource(Measurement, '/measurement')
api.add_resource(Room, '/rooms')
api.add_resource(Sensor, '/sensors')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=2000, debug=True)
