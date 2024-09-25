import os
import glob
import time
import board
import busio
import adafruit_max30102
import adafruit_ds18x20
import adafruit_onewire.bus

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

def read_sensor_data():
    while True:
        temp = read_temp()
        print("Temperature: {:.2f} C".format(temp))
        
        red, ir = max30102_sensor.read()
        print("Red LED: {}, IR LED: {}".format(red, ir))
        
        time.sleep(1)

if __name__ == "__main__":
    read_sensor_data()
