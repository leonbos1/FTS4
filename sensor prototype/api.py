from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, marshal_with, fields
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

app = Flask(__name__)
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)

class DistanceModel(db.Model):
    __tablename__ = 'distance'
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Integer)
    date = db.Column(db.String)
    time = db.Column(db.String)



class Distance(Resource):
    def get(self):
        return {
            'hello': 'world'
            }

    def post(self):
        data = request.get_json(force=True)
        print(data)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M:%S")

        distance = DistanceModel()
        distance.distance = data['distance']
        distance.date = date
        distance.time = time

        db.session.add(distance)
        db.session.commit()


        return {
            'data': data
            }

api.add_resource(Distance, '/distance')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='192.168.178.69',port=2000, debug=True, threaded=True)