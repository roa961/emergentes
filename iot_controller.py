from db import connect_db
from db import create_tables

connect_db()
create_tables()

def get_all_location():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM location""")
    return cursor.fetchall()
def get_all_sensor():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM sensor""")
    return cursor.fetchall()
def get_all_sensor_data():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM sensor_data""")
    return cursor.fetchall()