#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import TSjson
from os import path
from sys import exit
from sys import argv as sys_argv
from time import sleep
from clientmqtt import ClientMQTT

####################################################################################################

# Actual constant.py full path
SCRIPT_PATH = path.dirname(path.realpath(__file__))

# Files Path
F_CONFIG_MQTT = SCRIPT_PATH + "/cfg/mqtt.json"
F_TOPICS_TO_SUBS = SCRIPT_PATH + "/cfg/rx_subs_topics.txt"

####################################################################################################

mqttc = None

####################################################################################################

def load_config_from_file(file_path):
    '''Load configs from json file.'''
    print("Loading config data from file {}".format(file_path))
    cfg_file = TSjson.TSjson(file_path)
    cfg = cfg_file.read()
    # Check if file is empty
    if (cfg is None) or (cfg == {}):
        print("File doesn't exists, is empty or has invalid content.")
        finish(1)
    return cfg


def load_mqtt_configs(file_path):
    '''Load MQTT configs from JSON file.'''
    # Read from file
    mqtt_configs = load_config_from_file(file_path)
    # Show loaded data
    print("MQTT config successfully loaded:")
    print("  MQTT HOST: {}".format(mqtt_configs["HOST"]))
    print("  MQTT PORT: {}".format(mqtt_configs["PORT"]))
    if mqtt_configs["USER"] != "":
        print("  MQTT USER: {}".format(mqtt_configs["USER"]))
    if mqtt_configs["PASS"] != "":
        print("  MQTT PASS: {}".format(mqtt_configs["PASS"]))
    if mqtt_configs["CLIENTID"] != "":
        print("  MQTT CLIENT ID: {}".format(mqtt_configs["CLIENTID"]))
    print("")
    return mqtt_configs


def load_mqtt_topics_to_subscribe(file_path):
    '''Load list of MQTT topics to subscribe the controller from config txt file.'''
    list_topics = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                if line is None:
                    continue
                if (line == "") or (line == "\r\n") or (line == "\r") or (line == "\n"):
                    continue
                line = line.replace("\r", "")
                line = line.replace("\n", "")
                list_topics.append(line)
    except Exception as e:
        print("Error when opening file \"{}\". {}".format(file_path, str(e)))
        finish(1)
    if len(list_topics) == 0:
        print("No topics found in file \"{}\".".format(file_path))
        finish(1)
    return list_topics


def mqtt_on_received(mqttc, topics, obj, msg):
    '''MQTT received message callback.'''
    print("MQTT message received")
    print("Message: {}".format(msg))
    print("Topic: {}".format(msg.topic))
    print("Payload:")
    print(msg.payload)
    print("")

####################################################################################################

### Main and Finish Functions ###

def main(argv):
    '''Main Function.'''
    print("")
    # Load configs from files
    mqtt_configs = load_mqtt_configs(F_CONFIG_MQTT)
    topics_to_subs = load_mqtt_topics_to_subscribe(F_TOPICS_TO_SUBS)
    # MQTT client launch
    mqttc = ClientMQTT(client_id=mqtt_configs["CLIENTID"], clean_session=True)
    mqttc.launch(mqtt_configs["HOST"], mqtt_configs["PORT"], user=mqtt_configs["USER"], log=True, \
                 passw=mqtt_configs["PASS"], topics=topics_to_subs, rxcallback=mqtt_on_received)
    while True:
        sleep(1)
    finish(0)


def finish(return_code):
    '''Finish function.'''
    global mqttc
    # Close MQTT connection if it is used
    if mqttc is not None:
        mqttc.end()
    print("")
    exit(return_code)

####################################################################################################

### Script Input - Main Script ###

if __name__ == "__main__":
    try:
        main(sys_argv[1:])
    except KeyboardInterrupt:
        finish(1)
