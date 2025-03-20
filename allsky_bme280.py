'''
allsky_bme280.py

Coding Marco Lorenzi
directory name must be "allsky_bme280" and should include the related requirements.txt file

'''
import allsky_shared as s
import os
import math
import board
from adafruit_bme280 import basic as adafruit_bme280


metaData = {
    "name": "Climate data",
    "description": "Read data from environment sensor BME280",
    "module": "allsky_bme280",
    "version": "v1.0.0",    
    "events": [
        "night",
        "day"
    ],
    "experimental": "true",    
    "arguments":{
        "select": "0x76"
    },
        "argumentdetails": {
        "select" : {
            "required": "true",
            "description": "I2C Address bme280",
            "help": "Override the standard i2c address for a device.",
            "tab": "Sensor",
            "type": {
                "fieldtype": "select",
                "values": "0x76,0x77",
                "default": "0x76"
            }                
        }
    },
    "enabled": "true"            
}

def bme280(params, event):
    i2caddress = params["select"]
    extraData = {}
    tamb = None
    hum = None
    baro = None
    dewp = None

    i2c = board.I2C()
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, int(i2caddress, 16))

    tamb = bme280.temperature
    hum = bme280.humidity
    A = 17.27
    B = 237.7
    C = ((A * tamb) / (B + tamb)) + math.log(hum/100.0)
    dewp = (B * C) / (A - C)
    baro = round(bme280.pressure,0)
 
    extraData["BME_BAROPRES"] = str(baro)
    extraData["BME_TAMBIENT"] = str(tamb)
    extraData["BME_HUMIDITY"] = str(hum)
    extraData["BME_DEWPOINT"] = str(dewp)
    s.saveExtraData("allskybme280.json", extraData)
  
    climadata = "BaroPressure {0}, Ambient {1}, Humidity {2}, Dew Point {3}".format(baro, tamb, hum, dewp)
    s.log(1, "INFO: {}".format(climadata))

    return climadata

def bme280_cleanup():
    moduleData = {
        "metaData": metaData,
        "cleanup": {
            "files": {
                "allskybme280.json"
            },
            "env": {}
        }
    }
    s.cleanupModule(moduleData)
