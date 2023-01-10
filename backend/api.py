from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api, marshal_with, fields, reqparse
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import random
from time import sleep

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


class SituationModel(db.Model):
    __tablename__ = 'situation'
    id = db.Column(db.Integer, primary_key=True)
    situation = db.Column(db.String)
    time = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


SituationModelMarshal = {
    'id': fields.Integer,
    'situation': fields.String,
    'time': fields.String,
    'room_id': fields.Integer,
    'room_name': fields.String,
    'occupants': fields.Integer
}


class RoomModel(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class PersonModel(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    heart_rate = db.Column(db.Integer)
    behaviour = db.Column(db.String)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


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

# Data generator


def generate_data(situation_id: int):
    # hier situatie ophalen. als er een situatie is, dan moet er data gegenereerd worden.
    # als er geen situatie is, gewoon return
    situation = SituationModel.query.filter_by(id=situation_id).first()

    if not situation:
        return

    room = RoomModel.query.filter_by(id=situation.room_id).first()

    # alle mensen in een room
    people = PersonModel.query.filter_by(room_id=room.id).all()

    # als er geen mensen zijn: zet er mensen in.
    if not people:

        situation_name = situation.situation.lower()

        if situation_name == "hostage":
            amount_of_people = random.randint(1, 10)
            amount_of_aggresive_people = random.randint(1, 4)

        elif situation_name == "intruder":
            amount_of_people = random.randint(0, 4)
            amount_of_aggresive_people = random.randint(1, 4)

        elif situation_name == "medical emergency":
            amount_of_people = 1
            amount_of_aggresive_people = 0

        elif situation_name == "fire":
            amount_of_people = random.randint(0, 2)
            amount_of_aggresive_people = 0

        elif situation_name == "aggression":
            amount_of_people = 1
            amount_of_aggresive_people = 1
        
        else:
            amount_of_people = 1
            amount_of_aggresive_people = 1

        for i in range(amount_of_people):
            person = generate_person(False, room.id)
            db.session.add(person)

        for i in range(amount_of_aggresive_people):
            person = generate_person(True, room.id)
            db.session.add(person)
        db.session.commit()

    # als er mensen zijn: update de heart rate een beetje
    if len(people) > 0:
        for person in people:
            if person.behaviour == "aggressive":
                person.heart_rate = random.randint(120, 150)
            else:
                person.heart_rate = random.randint(80, 100)


def generate_person(is_dangerous: bool, room_id: int):

    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Kevin", "Linda",
             "Mike", "Nancy", "Oscar", "Peggy", "Quentin", "Ruth", "Steve", "Trudy", "Victor", "Wendy", "Xavier", "Yvonne", "Zach"]

    name = random.choice(names)

    if is_dangerous:
        return PersonModel(
            name=name,
            heart_rate=random.randint(120, 150),
            behaviour="aggressive",
            room_id=room_id
        )

    return PersonModel(
        name=name,
        heart_rate=random.randint(80, 100),
        behaviour="normal",
        room_id=room_id
    )

    # Routes


@app.route("/demo", methods=["GET"])
def get_demo():
    demo = DemoModel.query.order_by(DemoModel.id.desc()).first()
    # make json with demo demo
    result = {'demo': demo.demo}

    return result

@app.route("/generate", methods=["POST"])
def test_generate():
    input_json = request.get_json(force=True)
    situation_id = input_json['situation_id']
    generate_data(situation_id)
    return 'succes', 200

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

@app.route("/status", methods=["GET"])
def status():
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

        # generate_data(data['sensor_id'])

        measurement_model = MeasurementModel()
        measurement_model.distance = data['distance']
        measurement_model.sound = data['sound']
        measurement_model.date = date
        measurement_model.time = time
        measurement_model.sensor_id = data['sensor_id']

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


class Situation(Resource):
    @marshal_with(SituationModelMarshal)
    def get(self):
        situation = SituationModel.query.all()

        for s in situation:

            people_in_room = PersonModel.query.filter_by(room_id=s.room_id).all()
            s.occupants = len(people_in_room)
            print(s.occupants)

            room = RoomModel.query.filter_by(id=s.room_id).first()
            s.room_name = room.name
            
        return situation

    def post(self):
        data = request.get_json(force=True)
        time = datetime.datetime.now().strftime("%H:%M:%S")

        situation_model = SituationModel()
        situation_model.situation = data['situation']
        situation_model.time = time
        situation_model.room_id = data['room_id']
        db.session.add(situation_model)
        db.session.commit()

        generate_data(situation_model.id)

        return 'Succes', 200

    def delete(self):
        data = request.get_json(force=True)

        if data['all'] == True:
            #remove all situations
            situation_model = SituationModel.query.all()
            #remove all people
            person_model = PersonModel.query.all()
            for person in person_model:
                db.session.delete(person)
            for situation in situation_model:
                db.session.delete(situation)
            db.session.commit()
            return 'Succes', 200

        situation_model = SituationModel.query.filter_by(id=data['id']).first()

        persons = PersonModel.query.filter_by(room_id=situation_model.room_id).all()

        for person in persons:
            db.session.delete(person)
            
        db.session.delete(situation_model)
        db.session.commit()

        return 'Succes', 200


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
api.add_resource(Situation, '/situations')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=2000, debug=True)
