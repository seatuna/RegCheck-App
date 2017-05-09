#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
""" Python application for registration and check-in at events """
from flask import Flask, request, json, abort
from sqlalchemy import create_engine, exc

# configure application
APP = Flask(__name__)

# connect db
DB = create_engine("sqlite:///travcon.db")

@APP.route("/entrants", methods=["GET", "POST", "PATCH", "DELETE"])
def entrants():
    """ GET, POST, PATCH, and DELETE entrants for event registration """

    # connect to DB and start transaction
    connection = DB.connect()
    transaction = connection.begin()

    # get data for POST / PATCH / DELETE requests
    if request.json:
        submitted_data = request.json["entrants"]
        success_message = request.method + " successful!\n"

    # POST Request. Create new entry, commit, and close connection if successful, rollback if error.
    if request.method == "POST":
        name = submitted_data["name"]
        city = submitted_data["city"]
        state = submitted_data["state"]

        try:
            connection.execute("INSERT INTO entrants (name, city, state) \
                VALUES (:name, :city, :state)", name=name, city=city, state=state)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # PATCH Request. Update an entry, commit, and close connection if successful, rollback if error.
    elif request.method == "PATCH":
        entrant_id = submitted_data["id"]
        name = submitted_data["name"]
        city = submitted_data["city"]
        state = submitted_data["state"]

        try:
            connection.execute("UPDATE entrants SET name = :name, city = :city, state = :state \
                        WHERE id = :entrant_id", name=name, city=city, state=state,
                               entrant_id=entrant_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # DELETE Request for entrants
    elif request.method == "DELETE":
        entrant_id = submitted_data["id"]

        try:
            connection.execute("DELETE FROM entrants WHERE id = :entrant_id", entrant_id=entrant_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # GET Request for entrants
    else:
        query = connection.execute("SELECT * FROM entrants")
        return json.dumps({"entrants": [dict(row) for row in query]}), 201

@APP.route("/venues", methods=["GET", "POST", "PATCH", "DELETE"])
def venues():
    """ GET, POST, PATCH, and DELETE venues for event registration """

     # connect to DB and start transaction
    connection = DB.connect()
    transaction = connection.begin()

    # get data for POST / PATCH / DELETE requests
    if request.json:
        submitted_data = request.json["venues"]
        success_message = request.method + " successful!\n"

    # POST Request. Create new entry, commit, and close connection if successful, rollback if error.
    if request.method == "POST":
        name = submitted_data["name"]
        address = submitted_data["address"]
        city = submitted_data["city"]
        state = submitted_data["state"]

        try:
            connection.execute("INSERT INTO venues (name, address, city, state) \
                VALUES (:name, :address, :city, :state)", name=name, address=address,
                               city=city, state=state)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # PATCH Request. Update entry, commit, and close connection if successful, rollback if error.
    elif request.method == "PATCH":
        venue_id = submitted_data["id"]
        name = submitted_data["name"]
        address = submitted_data["address"]
        city = submitted_data["city"]
        state = submitted_data["state"]

        try:
            connection.execute("UPDATE venues SET name = :name, address = :address, \
            city = :city, state = :state WHERE id = :venue_id", name=name, address=address,
                               city=city, state=state, venue_id=venue_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # DELETE Request. Delete entry, commit, and close connection if successful, rollback if error.
    elif request.method == "DELETE":
        venue_id = submitted_data["id"]

        try:
            connection.execute("DELETE FROM venues WHERE id = :venue_id", venue_id=venue_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # GET Request for venues
    else:
        query = connection.execute("SELECT * FROM venues")
        return json.dumps({"venues": [dict(row) for row in query]}), 201

@APP.route("/venues/<int:venue_id>/events", methods=["GET"])
def get_events_by_venue(venue_id):
    """ GET events associated with a specified venue """

     # connect to DB and start transaction
    connection = DB.connect()
    transaction = connection.begin()

    if request.json:
        submitted_data = request.json["events_by_venue"]
        success_message = request.method + " successful!\n"

    try:
        event_id = submitted_data["event_id"]
        query = connection.execute("SELECT * FROM events WHERE venue_id = :venue_id", venue_id=venue_id)
        return json.dumps({ "events": [dict(row) for row in query] }), 201
    except exc.SQLAlchemyError as error:
        transaction.rollback()
        print(error)
        abort(400)
    finally:
        connection.close()

@APP.route("/events", methods=["GET", "POST", "PATCH", "DELETE"])
def events():
    """ GET, POST, PATCH, and DELETE venues for event registration """

    # connect to DB and start transaction
    connection = DB.connect()
    transaction = connection.begin()

    # get data for POST / PATCH / DELETE requests
    if request.json:
        submitted_data = request.json["events"]
        success_message = request.method + ' successful!\n'

    # POST Request for events
    if request.method == "POST":
        name = submitted_data["name"]
        description = submitted_data["description"]
        games = submitted_data["games"]
        venue_id = submitted_data["venue_id"]

        try:
            connection.execute("INSERT INTO events (name, description, games, venue_id) \
                    VALUES (:name, :description, :games, :venue_id)", name=name,
                               description=description, games=games, venue_id=venue_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # PATCH Request for events
    elif request.method == "PATCH":
        event_id = submitted_data["id"]
        name = submitted_data["name"]
        description = submitted_data["description"]
        games = submitted_data["games"]
        venue_id = submitted_data["venue_id"]

        try:
            connection.execute("UPDATE events SET name = :name, description = :description, \
            games = :games, venue_id = :venue_id WHERE id = :event_id", name=name,
                               description=description, games=games, venue_id=venue_id,
                               event_id=event_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # DELETE Request for events
    elif request.method == "DELETE":
        event_id = submitted_data["id"]

        try:
            connection.execute("DELETE FROM events WHERE id = :event_id", event_id=event_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # GET Request for events
    else:
        query = connection.execute("SELECT * FROM events")
        return json.dumps({"events": [dict(row) for row in query]}), 201

@APP.route("/events_entrants", methods=["GET", "POST", "DELETE"])
def events_entrants():
    """ GET, POST, DELETE for events_entrants join table """
    # connect to DB and start transaction
    connection = DB.connect()
    transaction = connection.begin()

    # get data for POST / PATCH / DELETE requests
    if request.json:
        submitted_data = request.json["events_entrants"]
        success_message = request.method + ' successful!\n'

    # POST Request for events
    if request.method == "POST":
        entrant_id = submitted_data["entrant_id"]
        event_id = submitted_data["event_id"]

        try:
            connection.execute("INSERT INTO events_entrants (event_id, entrant_id) \
                    VALUES (:event_id, :entrant_id)", event_id=event_id, entrant_id=entrant_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # DELETE Request for events
    elif request.method == "DELETE":
        entrant_id = submitted_data["entrant_id"]
        event_id = submitted_data["id"]

        try:
            connection.execute("DELETE FROM events_entrants WHERE event_id = :event_id \
                    AND entrant_id = :entrant_id", event_id=event_id, entrant_id=entrant_id)
            transaction.commit()
            return success_message, 201
        except exc.SQLAlchemyError as error:
            transaction.rollback()
            print(error)
            abort(400)
        finally:
            connection.close()

    # GET Request for events
    else:
        query = connection.execute("SELECT * FROM events_entrants")
        return json.dumps({"events_entrants": [dict(row) for row in query]}), 201

@APP.route("/events/<int:event_id>", methods=["GET"])
def get_event_details(event_id):
    """ GET, POST, PATCH, DELETE event details and entrants """

    # connect to DB and start transaction
    connection = DB.connect()
    transaction = connection.begin()

    if request.method == "GET":
        query = connection.execute("SELECT * FROM events_entrants WHERE event_id = :event_id", event_id=event_id)
        return json.dumps({"events": [dict(row) for row in query]}), 201