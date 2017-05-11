#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
'''SQL code for seeding the travcon database'''
import sqlite3

def main():
    '''Connect to db and create tables'''
    database = sqlite3.connect('./travcon.db')

    insert_venue1 = '''INSERT INTO venues (name, address, city, state) VALUES \
                    ("HES", "123 Harvard Sq", "Cambridge", "MA")'''

    insert_venue2 = '''INSERT INTO venues (name, address, city, state) VALUES \
                    ("Game Underground", "Natick Mall", "Natick", "MA")'''

    insert_event1 = '''INSERT INTO events (name, description, games, venue_id) VALUES \
                     ("TC Event 1", "The first one ever", "Street Fighter, Guilty Gear", 2)'''

    insert_event2 = '''INSERT INTO events (name, description, games, venue_id) VALUES \
                     ("Different Event", "A completely different event", "Super Smash Bros", 2)'''

    insert_event3 = '''INSERT INTO events (name, description, games, venue_id) VALUES \
                     ("Tuna Games", "The stuff I would play", "Puzzle Figher, Bomberman, \
                     Puyo Puyo", 1)'''

    insert_entrant1 = '''INSERT INTO entrants (name, city, state) VALUES \
                      ("seatuna222", "Brighton", "MA")'''
    insert_entrant2 = '''INSERT INTO entrants (name, city, state) VALUES \
                      ("LuckyD222", "Boston", "MA")'''
    insert_entrant3 = '''INSERT INTO entrants (name, city, state) VALUES \
                      ("asiantom222", "Winchester", "MA")'''

    insert_events_entrants1 = '''INSERT INTO events_entrants (event_id, entrant_id) VALUES (1,1)'''
    insert_events_entrants2 = '''INSERT INTO events_entrants (event_id, entrant_id) VALUES (1,2)'''
    insert_events_entrants3 = '''INSERT INTO events_entrants (event_id, entrant_id) VALUES (1,3)'''
    insert_events_entrants4 = '''INSERT INTO events_entrants (event_id, entrant_id) VALUES (2,3)'''
    insert_events_entrants5 = '''INSERT INTO events_entrants (event_id, entrant_id) VALUES (2,1)'''

    # create venues, events, entrants tables if db connection is successful
    if database is not None:
        cursor = database.cursor()
        cursor.execute(insert_venue1)
        cursor.execute(insert_venue2)
        cursor.execute(insert_event1)
        cursor.execute(insert_event2)
        cursor.execute(insert_event3)
        cursor.execute(insert_entrant1)
        cursor.execute(insert_entrant2)
        cursor.execute(insert_entrant3)
        cursor.execute(insert_events_entrants1)
        cursor.execute(insert_events_entrants2)
        cursor.execute(insert_events_entrants3)
        cursor.execute(insert_events_entrants4)
        cursor.execute(insert_events_entrants5)
        database.commit()
    else:
        print('Can\'t connect to database')

if __name__ == '__main__':
    main()
    