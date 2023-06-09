from flask import Flask, jsonify, request
import iot_controller 

app = Flask(__name__)
@app.route('/location', methods=["GET"])
def get_location():
    locations = iot_controller.get_all_location()
    return jsonify(locations)

@app.route('/sensor', methods=["GET"])
def get_sensor():
    sensors = iot_controller.get_all_sensor()
    return jsonify(sensors)


