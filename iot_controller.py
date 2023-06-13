from db import connect_db
from db import create_tables
from flask import Flask, jsonify, request, session, Response, json
import time


create_tables()


def company_create(name, key):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("insert into company(company_name, company_api_key) values(?,?) ",(name, str(key)))
    db.commit()
    return cursor.fetchall()

def get_all_company():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM company""")
    return cursor.fetchall()

def get_one_company(company_key):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM company where company_api_key = ? """, (company_key,))
    return cursor.fetchall()

def edit_one_company(company_name, key):
    db = connect_db()
    cursor = db.cursor()
    try: 
        cursor.execute("""UPDATE company SET company_name = ? where company_api_key = ? """,(str(company_name), str(key)))
        db.commit()
        return {"Nuevo nombre": company_name}
    except:
        print("no editado")
def del_company(company_name, key):
    db = connect_db()
    cursor = db.cursor()
    try: 
        cursor.execute("""delete from company where company_api_key = ? and  company_name = ?""",(str(key), str(company_name)))
        db.commit()
        return cursor.fetchall()
    except:
        print("no borrado")

def get_user_pass(user, passw):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT CASE WHEN EXISTS (SELECT *  FROM admin where username = ? and password = ?) THEN 1 ELSE 0 END AS BIT""", (user, passw ))
    return cursor.fetchone()[0]

def location_create(key, name, country, city, meta):
    db = connect_db()
    cursor = db.cursor()
    company_id = cursor.execute("""SELECT company.id FROM company where company_api_key = ? """, (key,)).fetchone()[0]
    print(company_id)
    cursor.execute("insert into location(company_id, location_name, location_country, location_city, location_meta ) values(?,?,?,?,?) ",(company_id, name, country, city, meta))
    db.commit()
    return {"Lugar creado": name}


def get_all_location():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM location""")
    return cursor.fetchall()

def get_one_location(company_key, location_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT location.ID, location.company_id, location.location_name, location_country, location_city, location_meta FROM location, company where company_api_key = ? and company.ID = location.company_id and location.location_name = ? """, (company_key, location_name))
    return cursor.fetchall()

def edit_location(key, old_name,name, country, city, meta):
    db = connect_db()
    cursor = db.cursor()
    try:
        company_id = cursor.execute("""SELECT company.id FROM company where company_api_key = ? """, (key,)).fetchone()[0]
 
        cursor.execute("""UPDATE location SET location_name = ?, location_country = ?, location_city = ?, location_meta = ? where company_id = ? and location_name = ?""",(name, country, city, meta, company_id, old_name))
        db.commit()
        cursor.execute("""Select * from location where location_name = ?""", (name,))
        return cursor.fetchall()
    except:
        print("no editado")

def del_location(location_name, key):
    db = connect_db()
    cursor = db.cursor()
    try:
        print(location_name)
        print(key)
        company_id = cursor.execute("""SELECT company.id FROM company where company_api_key = ? """, (key,)).fetchone()[0]
        print(company_id)
        cursor.execute("""delete from location where company_id = ? and location_name = ?""",(company_id, location_name))
        db.commit()
        return {"Localizacion borrada": location_name}
    except:
        print("no borrado")


def sensor_create(location_name, company_key, sensor_name, sensor_category, sensor_meta, sensor_key):
    db = connect_db()
    cursor = db.cursor()
    location_id = cursor.execute("""SELECT location.id FROM location, company where company_id = company.id and company_api_key = ? and location_name = ?""" , (company_key, location_name)).fetchone()[0]
    print(location_id)
    cursor.execute("insert into sensor(location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key ) values(?,?,?,?,?) ",(location_id, sensor_name, sensor_category, sensor_meta, sensor_key))
    db.commit()
    cursor.execute("""Select * from sensor where sensor_api_key = ? """, (sensor_key,))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))

    json_data = json.dumps(data)
    return json_data



def get_all_sensor():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM sensor""")
    return cursor.fetchall()

def get_one_sensor(company_key, sensor_name):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM sensor where sensor_name = ?  """, (sensor_name,))
    return cursor.fetchall()


def edit_sensor(company_key, sensor_id, sensor_name, sensor_category, sensor_meta,):
    db = connect_db()
    cursor = db.cursor()
    try:
        senkey_id = cursor.execute("""SELECT sensor_api_key FROM sensor where sensor_ID = ? """, (sensor_id,)).fetchone()[0] 
        cursor.execute("""UPDATE SENSOR SET sensor_name = ?, sensor_category = ?, sensor_meta = ? where sensor_api_key = ? """,(sensor_name, sensor_category, sensor_meta, senkey_id))
        db.commit()
        cursor.execute("""Select * from sensor where sensor_api_key = ?""", (senkey_id,))

        return cursor.fetchall()
    except:
        print("no editado")



def del_sensor(sensor_id, key):
    db = connect_db()
    cursor = db.cursor()
    try:
        sensor_ded = \
            cursor.execute("""select sensor_name from sensor where sensor_id = ?"""
                           , (sensor_id, )).fetchone()[0]
        cursor.execute("""delete from sensor where sensor_id = ?""",
                       (sensor_id, ))
        db.commit()
        return {"Sensor borrado": sensor_ded, "sensor_id": sensor_id}
    except:

        print ("no borrado")



def post_sensor(sensor_api_key, datos, epoch_time):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("insert into sensor_data(sensor_api_key, json_data, time) values(?,?,?) ",(sensor_api_key, datos, str(epoch_time)))
    db.commit()
    data = {'Ingresado': '1', 'epoch_time':epoch_time}
    json.dumps(data)
    return Response(json.dumps(data), status=201, mimetype='application/json')

def get_sensor(company_key, from_time, to_time, sensor_id ):
    db = connect_db()
    cursor = db.cursor()
    print(from_time)
    sensor_id.append(from_time)
    sensor_id.append(to_time)
    evaluar = cursor.execute("SELECT CASE WHEN EXISTS (SELECT *  FROM company where company_api_key = ? ) THEN 1 ELSE 0 END AS BIT",(company_key,))
    largo = len(sensor_id) - 2
    query = "select sensor_data.json_data, time from sensor, sensor_data where sensor.sensor_api_key = sensor_data.sensor_api_key and sensor.sensor_id IN("
    query += ",".join(["?"] * largo)
    query += ") and time >= ? and time <= ?"
    cursor.execute(query,tuple(sensor_id))

    return cursor.fetchall()
