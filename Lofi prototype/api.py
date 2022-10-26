from cgitb import reset
from math import degrees
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, marshal_with, fields
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps

app = Flask(__name__)
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SECRET_KEY'] = 'secretkey'
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
db = SQLAlchemy(app)



class Distance(Resource):
    def get(self):
        return {
            'hello': 'world'
            }

    def post(self):
        data = request.get_data()
        print(data)

        return {
            'data': data
            }

api.add_resource(Distance, '/distance')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='192.168.178.69',port=2000, debug=True, threaded=True)