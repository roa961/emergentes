from flask import Flask, jsonify, request, session, Response, json
import time 
import iot_controller 
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'iot'


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    rest = iot_controller.get_user_pass(username, password)
    if rest == 1:
         session['username'] = username
         return jsonify({'message': 'Sesión de ' + username + ' iniciada!'})
    elif rest == 0:
        return jsonify({'message': 'Credenciales inválidas'})
    
@app.route('/profile')
def profile():
    if 'username' in session:
        return True
    else:
        return False
    

###################


## Company CRUD

#Create company
@app.route('/create-company', methods=["POST"])
def create_company():
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    data = request.get_json()

    Id = str(random.randint(1000,9999))
    company_name = data.get('company_name')
    company_api_key = Id + company_name + str(random.randint(1000,9999))
    try:
        iot_controller.company_create(company_name, company_api_key)
        return jsonify({"Company key": company_api_key})

    except:
        return Response("{'a':'b'}", status=400, mimetype='application/json')
    
#Get all companies
@app.route('/getCompany', methods=["GET"])
def get_company():
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    companies = iot_controller.get_all_company()
    return jsonify(companies)

#Get one company
@app.route('/getOneCompany', methods=["GET"])
def get_one_company():
    company_key = request.args.get('key')
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company = iot_controller.get_one_company(company_key)
    return jsonify(company)

#edit company name
@app.route('/editCompany', methods=["PUT"])
def edit_company():
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    data = request.get_json()
    new_company = data.get('company_name')
    edited = iot_controller.edit_one_company(new_company, company_key)
    return jsonify(edited)

#Delete company
@app.route('/deleteCompany', methods=["DELETE"])
def delete_company():
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    data = request.get_json()
    delete = data.get('company_name')
    iot_controller.del_company(delete, company_key)
    return jsonify({"Compañia": "borrada"})

###################


##Location CRUD

#Create location
@app.route('/create-location', methods=["POST"])
def create_location():
    data = request.get_json()
    location_name = data.get('location_name')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta')
    
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    try:
        res = iot_controller.location_create(company_key, location_name, location_country, location_city, location_meta)
        return jsonify(res)

    except:
        return Response("{'a':'b'}", status=400, mimetype='application/json')

#Get location
@app.route('/getlocation', methods=["GET"])
def get_location():
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    locations = iot_controller.get_all_location()
    return jsonify(locations)

#Get one location
@app.route('/getlocation_one', methods=["GET"])
def get_one_location():
    data = request.get_json()
    location_name = data.get('location_name')
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    location_one = iot_controller.get_one_location(company_key, location_name)
    return jsonify(location_one)

#Edit location
@app.route('/editLocation', methods=["PUT"])
def edit_location():
    data = request.get_json()
    old_name = data.get('old_name')
    location_name = data.get('location_name')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta')
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    data = request.get_json()
    edited = iot_controller.edit_location(company_key, old_name,location_name, location_country, location_city, location_meta)
    return jsonify(edited)

#Delete location
@app.route('/deleteLocation', methods=["DELETE"])
def delete_location():
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    data = request.get_json()
    delete = data.get('location_name')
    deleted = iot_controller.del_location(delete, company_key)
    return jsonify(deleted)

###################


##Sensor CRUD

#Create sensor
@app.route('/create-sensor', methods=["POST"])
def create_sensor():
    data = request.get_json()
    location_name = data.get('location_name')
    sensor_name = data.get('sensor_name')
    sensor_category = data.get('sensor_category')
    sensor_meta = data.get('sensor_meta')

    Id = str(random.randint(1000,9999))
    sensor_name = data.get('sensor_name')
    sensor_api_key = Id + sensor_name + str(random.randint(1000,9999))
    
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    try:
       details = iot_controller.sensor_create(location_name, company_key, sensor_name, sensor_category, sensor_meta, sensor_api_key)
       return details

    except:
        return Response("{'a':'b'}", status=400, mimetype='application/json')

#Get  all sensors
@app.route('/sensor', methods=["GET"])
def get_sensor():
    sensors = iot_controller.get_all_sensor()
    return jsonify(sensors)


### Get one
@app.route('/sensorOne', methods=["GET"])
def get_sensor_one():
    data = request.get_json()
    sensor_name = data.get('sensor_name')
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    sensors = iot_controller.get_one_sensor(company_key, sensor_name)
    return jsonify(sensors)

#Edit Sensor
@app.route('/editSensor', methods=["PUT"])
def edit_sensor():
    data = request.get_json()
    sensor_name = data.get('sensor_name')
    sensor_category = data.get('sensor_category')
    sensor_meta = data.get('sensor_meta')
    sensor_id = data.get('sensor_id')

    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    data = request.get_json()
    edited_sens = iot_controller.edit_sensor(company_key, sensor_id,sensor_name, sensor_category, sensor_meta)
    return jsonify(edited_sens)

#Delete sensor
@app.route('/deleteSensor', methods=["DELETE"])
def delete_sensor():
    if not profile():
        return jsonify({'message': 'Necesitas iniciar sesión'})
    company_key = request.args.get('key')
    data = request.get_json()
    sensor_id = data.get('sensor_id')
    borrado = iot_controller.del_sensor(sensor_id, company_key)
    print(borrado)
    return jsonify(borrado)

##Sensor data

###Create
@app.route('/api/v1/sensor_data', methods=["POST"])
def post_sensor_data_temper():
    sensor_api_key = request.args.get('key')
    data = request.get_json()
    epoch_time = int(time.time())
    jsonData = json.dumps(data)
    sensors = iot_controller.post_sensor(sensor_api_key, jsonData, epoch_time)
    return sensors

### Get data
@app.route('/api/v1/sensor_data', methods=["GET"])
def get_sensor_data():
    company_key = request.args.get('key')
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    sensor_id = request.args.get('sensor_id')
    sensors = iot_controller.get_sensor(company_key, from_time, to_time, eval(sensor_id) )
    return jsonify(sensors)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
