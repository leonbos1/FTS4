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
    distance = db.Column(db.Float)
    sound = db.Column(db.Float)
    date = db.Column(db.String)
    time = db.Column(db.String)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'))


class RoomModel(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class SensorModel(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class DemoModel(db.Model):
    __tablename__ = 'demo'
    id = db.Column(db.Integer, primary_key=True)
    demo = db.Column(db.String)


measurement_field = {
    'id': fields.Integer,
    'distance': fields.Float,
    'sound': fields.Float,
    'date': fields.String,
    'time': fields.String,
    'sensor_id': fields.Integer
}

room_field = {
    'id': fields.Integer,
    'name': fields.String
}

sensor_field = {
    'id': fields.Integer,
    'name': fields.String,
    'room_id': fields.Integer
}

demo_field = {
    'id': fields.Integer,
    'demo': fields.String
}

# Routes


@app.route("/demo", methods=["GET"])
def get_demo():
    demo = DemoModel.query.order_by(DemoModel.id.desc()).first()
    # make json with demo demo
    result = {'demo': demo.demo}

    return result


@app.route("/demo", methods=["POST"])
def post_demo():
    input_json = request.get_json(force=True)
    demo = input_json['test']
    data = DemoModel(
        demo=demo
    )
    db.session.add(data)
    db.session.commit()
    return 'succes', 200


class Demo(Resource):
    @marshal_with(demo_field)
    def get(self):
        demo = DemoModel.query.all()
        return demo

    @marshal_with(demo_field)
    def post(self):
        input_json = request.get_json(force=True)
        demo = input_json['test']
        data = DemoModel(
            demo=demo
        )
        db.session.add(data)
        db.session.commit()
        return data


class Measurement(Resource):
    @marshal_with(measurement_field)
    def get(self):
        # where today
        #date = datetime.datetime.now().strftime("%Y-%m-%d")
        #distance = DistanceModel.query.filter_by(date=date).all()
        distance = MeasurementModel.query.all()
        return distance

    @marshal_with(measurement_field)
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
    @marshal_with(room_field)
    def get(self):
        room = RoomModel.query.all()
        return room

    @marshal_with(room_field)
    def post(self):
        data = request.get_json(force=True)
        room_model = RoomModel()
        room_model.name = data['name']
        db.session.add(room_model)
        db.session.commit()

        return room_model

    @marshal_with(room_field)
    def delete(self):
        data = request.get_json(force=True)
        print(data)
        room_model = RoomModel.query.filter_by(id=data['id']).first()
        db.session.delete(room_model)
        db.session.commit()

        return room_model

    @marshal_with(room_field)
    def put(self):
        data = request.get_json(force=True)
        room_model = RoomModel.query.filter_by(id=data['id']).first()
        room_model.name = data['name']
        db.session.commit()

        return room_model


class Sensor(Resource):
    @marshal_with(sensor_field)
    def get(self):
        sensor = SensorModel.query.all()
        return sensor

    @marshal_with(sensor_field)
    def post(self):
        data = request.get_json(force=True)
        sensor_model = SensorModel()
        sensor_model.name = data['name']
        sensor_model.room_id = data['room_id']
        db.session.add(sensor_model)
        db.session.commit()

        return sensor_model

    @marshal_with(sensor_field)
    def delete(self):
        data = request.get_json(force=True)
        sensor_model = SensorModel.query.filter_by(id=data['id']).first()
        db.session.delete(sensor_model)
        db.session.commit()

        return sensor_model

    @marshal_with(sensor_field)
    def put(self):
        data = request.get_json(force=True)
        sensor_model = SensorModel.query.filter_by(id=data['id']).first()
        sensor_model.name = data['name']
        sensor_model.room_id = data['room_id']
        db.session.commit()

        return sensor_model


api.add_resource(Measurement, '/measurement')
api.add_resource(Room, '/rooms')
api.add_resource(Sensor, '/sensors')
api.add_resource(Demo, '/demo')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=2000, debug=True)
