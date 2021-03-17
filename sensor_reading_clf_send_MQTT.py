#!/usr/bin/env python

import grovepi
import time
import datetime

from grove_sound_config import *
from grove_light_config import *
from grove_led_config import *
from grove_gas_config import *
import json
import subprocess
from grove_dht_config import *

import paho.mqtt.client as paho

import numpy as np
import pandas as pd
# import any additional packages you may need

# sample interval of sensor readings in seconds
SAMPLE_INTERVAL = 3

# MQTT: Change this to your broker if required
#broker = "mqtt.eclipse.org"
broker = "test.mosquitto.org"
#broker = "broker.hivemq.com"
port = 1883

# Create client with unique name
client= paho.Client("SensorTestGP3")
client.connect(broker,port)
print("mqtt client initiated.....\n")
print("Sending data to broker via MQTT.....\n")

labelInfo=["Dim", "Normal", "Bright"]

# Write your classifier code here (numpy, pandas, sklearn are available)
# 'model' is the object contains the trained model

#print("Model Ready!")
#print("************************")
#print

# MQTT: Sends data to broker under topic: EE5132/GP3/<SensorName>
def sendToBroker(sensorName, value):
    moduleCode = "EE5132"
    #change this to your own group
    groupName = "GP3"
    
    topic = moduleCode + "/" + groupName + "/" + sensorName
    client.publish(topic, str(value))

while True:
    sensorReadings = []
    try:
        # Get current time
        ts=time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print st
        
        #MQTT
        sendToBroker('time', st)
        
# Get value from sound sensor
        sound_level = grovepi.analogRead(sound_sensor_port)
        print "Sound->", sound_level
        print
        sensorReadings.append(sound_level)
        
# Get value from light sensor
        light_intensity = grovepi.analogRead(light_sensor_port)
        print "light->", light_intensity
        print
        sensorReadings.append(light_intensity)
        
# Get values from multichannel gas sensor
        args = ("/usr/local/bin/gas" )
        popen = subprocess.Popen(args, stdout=subprocess.PIPE)
        popen.wait()

        output = popen.stdout.read()
        print output
        #mj = json.loads(output)
        #print "CO->", mj['CO']
        #print "NO2->", mj['NO2']
        #print "C3H8->", mj['C3H8']
        #print "C4H1O->", mj['C4H1O']
        #print "CH4->", mj['CH4']
        #print "H2->", mj['H2']
        #print "C2H5OH->", mj['C2H5OH']
        #print
        
        # Get value from temperature and humidity sensors
        [temperature,humidity] = grovepi.dht(dht_sensor_port, 1) #0 is blue dht sensor, 1 is white dht sensor
        print "temp->",temperature," hum->",humidity
        print
        sensorReadings.append(temperature)
        sensorReadings.append(humidity) 

# Send sensor readings to MQTT broker
        # MQTT
        sendToBroker('light_intensity', light_intensity)
        # Fill in for additional sensors
        sendToBroker('sound_level', sound_level)
        sendToBroker('temp', temperature)
        sendToBroker('hum', humidity)
        
# Prediction     
        sensorReadings = np.array([sensorReadings])
        predict = [1]
#       Replace the hard-coded predicted class above with your classifier outputs
#       e.g. predict = model.predict(sensorReadings)

        print(labelInfo[predict[0]])
        
        # Classifier: calculate probability estimates for 3 classes
        #predict_probability = model.predict_proba(sensorReadings)
        #print(predict_probability)
        #print
        
        print "---------------------"
        time.sleep(SAMPLE_INTERVAL)
        #quit()

    except IOError:
        print("Error reading from sensors")
    except KeyboardInterrupt:
        exit()
        