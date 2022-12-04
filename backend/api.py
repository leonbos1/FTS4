from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_restful import Resource, Api, marshal_with, fields
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
api = Api(app)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

class DistanceModel(db.Model):
    __tablename__ = 'distance'
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    sound = db.Column(db.Integer)
    date = db.Column(db.String)
    time = db.Column(db.String)

DistanceModelMarshal = {
    'id': fields.Integer,
    'distance': fields.Integer,
    'sound': fields.Integer,
    'date': fields.String,
    'time': fields.String
}

class Distance(Resource):

    @marshal_with(DistanceModelMarshal)
    def get(self):
        #where today
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        #distance = DistanceModel.query.filter_by(date=date).all()
        distance = DistanceModel.query.all()
        return distance

    def post(self):
        data = request.get_json(force=True)
        print(data)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")


        distancemodel = DistanceModel()
        distancemodel.distance = data['distance']
        distancemodel.sound = data['sound']
        distancemodel.date = date
        distancemodel.time = time
        
        db.session.add(distancemodel)
        db.session.commit()

        return {
            'data': data
            }

api.add_resource(Distance, '/distance')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=2000, debug=True)