#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
""" Python application for registration and check-in at events """
from flask import Flask, request, jsonify, abort
# from flask_restful import Resource, Api
from sqlalchemy import create_engine
# from json import dumps
# from flask.ext.jsonpify import jsonify

# configure application
APP = Flask(__name__)
# api = Api(app)

# connect db
DB = create_engine("sqlite:///travcon.db")

@APP.route("/entrants", methods=["GET", "POST"])
def enter():
    """ GET and POST entrants for event registration """
    connection = DB.connect()
    if request.method == "POST":
        name = request.form.get("name")
        city = request.form.get("city")
        state = request.form.get("state")

        if not name:
            abort(400)

        query = connection.execute("INSERT INTO entrants (name, city, state) \
                VALUES (:name, :city, :state)", name=name, city=city, state=state)
        return 201
    else:
        query = connection.execute("SELECT * FROM entrants")
        return jsonify({"entrants": query}), 201
