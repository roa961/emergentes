from db import connect_db
from db import create_tables

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
        return cursor.fetchall()
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

def get_all_location():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM location""")
    return cursor.fetchall()

def get_one_location(company_key):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT location.ID, location.company_id int, location.location_name, location_country, location_city, location_meta FROM location, company where company_api_key = ? """, (company_key,))
    return cursor.fetchall()

def get_all_sensor():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM sensor""")
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