#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
'''SQL code for creating the travcon database'''
import sqlite3

def main():
    '''Connect to db and create tables'''
    database = sqlite3.connect('./travcon.db')

    create_venues_table = '''CREATE TABLE venues (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                address TEXT,
                                city TEXT,
                                state TEXT
                            )'''

    create_events_table = '''CREATE TABLE events (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                description TEXT,
                                games TEXT,
                                venue_id INTEGER,
                                FOREIGN KEY (venue_id) REFERENCES venues (id)
                            )'''

    create_entrants_table = '''CREATE TABLE entrants (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                city TEXT,
                                state TEXT
                            )'''

    create_events_entrants_table = '''CREATE TABLE events_entrants (
                                        id INTEGER PRIMARY KEY,
                                        events_id INTEGER,
                                        entrants_id INTEGER,
                                        FOREIGN KEY (events_id) REFERENCES events (id),
                                        FOREIGN KEY (entrants_id) REFERENCES entrants (id)
                                    )'''

    # create venues, events, entrants tables if db connection is successful
    if database is not None:
        cursor = database.cursor()
        cursor.execute(create_events_table)
        cursor.execute(create_venues_table)
        cursor.execute(create_entrants_table)
        cursor.execute(create_events_entrants_table)
        database.commit()
    else:
        print('Can\'t connect to database')

if __name__ == '__main__':
    main()
    