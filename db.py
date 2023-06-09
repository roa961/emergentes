import sqlite3
DATABASE_NAME = "iot.db"


def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    tables = ["""
        CREATE TABLE IF NOT EXISTS admin (
    username STRING,
    password STRING
)
""",
"""CREATE TABLE IF NOT EXISTS company (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name STRING,
    company_api_key STRING)"""
,
"""CREATE TABLE IF NOT EXISTS location(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id int,
    location_name STRING,
    location_country STRING,
    location_city STRING,
    location_meta STRING,
    foreign key(company_id) references company(ID)
)"""
,
"""CREATE TABLE IF NOT EXISTS sensor(
    location_id int,
    sensor_id int,
    sensor_name string,
    sensor_category string,
    sensor_meta string,
    sensor_api_key string,
    foreign key(location_id) references location(ID)
)"""
,
"""CREATE TABLE IF NOT EXISTS sensor_data(
    sensor_api_key string,
    json_data text,
    foreign key(sensor_api_key) references sensor(sensor_api_key)
)"""

    ]
    db = connect_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
create_tables()