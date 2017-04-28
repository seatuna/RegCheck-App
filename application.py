from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask.ext.jsonpify import jsonify

# configure application
app = Flask(__name__)
api = Api(app)

# connect db
db = create_engine('sqlite:///travcon.db')