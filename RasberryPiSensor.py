import os
import glob
import time
from flask import Flask, jsonify
import board
import busio
import adafruit_max30102

app = Flask(__name__)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    temp_output = lines[1].split(' ')[9]
    temp_c = float(temp_output[2:]) / 1000.0
    return temp_c

i2c = busio.I2C(board.SCL, board.SDA)
max30102_sensor = adafruit_max30102.MAX30102(i2c)

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    temp = read_temp()
    red, ir = max30102_sensor.read()
    
    return jsonify({
        'temperature': temp,
        'red_led': red,
        'ir_led': ir
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
