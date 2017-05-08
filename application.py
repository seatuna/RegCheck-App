#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
""" Python application for registration and check-in at events """
from flask import Flask, request, jsonify, abort, json
# from flask_restful import Resource, Api
from sqlalchemy import create_engine
# from json import dumps
# from flask.ext.jsonpify import jsonify

# configure application
APP = Flask(__name__)
# api = Api(app)

# connect db
DB = create_engine("sqlite:///travcon.db")

@APP.route("/entrants", methods=["GET", "POST", "PATCH", "DELETE"])
def enter():
    """ GET, POST, PATCH, and DELETE entrants for event registration """
    connection = DB.connect()
    entrant_id = request.form.get("id")
    name = request.form.get("name")
    city = request.form.get("city")
    state = request.form.get("state")

    # Returns a message with the request in JSON format
    # if request.headers['Content-Type'] == 'application/json':
    #     return "JSON Message: " + json.dumps(request.json)

    # POST Request
    if request.method == "POST":
            # Return 400 error if no name on form
        if not name:
            abort(400)

        connection.execute("INSERT INTO entrants (name, city, state) \
            VALUES (:name, :city, :state)", name=name, city=city, state=state)
        return 201

    # PATCH Request
    elif request.method == "PATCH":
        connection.execute("UPDATE entrants SET name = :name, city = :city, state = :state \
                    WHERE id = :entrant_id", name=name, city=city, state=state,
                           entrant_id=entrant_id)
        return 201

    # DELETE Request
    elif request.method == "DELETE":
        connection.execute("DELETE FROM entrants WHERE id = :entrant_id", entrant_id=entrant_id)

    # GET Request
    else:
        query = connection.execute("SELECT * FROM entrants")
        return json.dumps([dict(row) for row in query]), 201

# @APP.route("/venues", methods=["GET", "POST", "PATCH", "DELETE"])
