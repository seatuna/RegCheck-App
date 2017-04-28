	
import sqlite3

db = sqlite3.connect('./travcon.db')

cursor = db.cursor()
cursor.execute(
    '''
        CREATE TABLE event (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT
        )
    '''
)
db.commit()